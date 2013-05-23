import os
from datetime import datetime
from django.core.mail import send_mail
from openbudget.settings.base import TEMP_FILES_DIR, ADMINS, EMAIL_HOST_USER
from openbudget.apps.transport.models import String
from openbudget.apps.transport.incoming.parsers import get_parser, get_parser_key


class BaseImporter(object):
    """Gets data out of files and into the database.

    This class is abstract and does not implement the `get_data` method.

    This class can handle any of the supported datasets for importing.

    At this stage, that means Budget Templates (template and related
    node objects), and Budgets/Actuals (Budget or Actual, and related
    items).

    The importer supports a lower level import by parsing the
    file name for meta data - useful while testing, so developers do
    not have to work with an interactive importer. Otherwise, \
    it should be used with an interactive wizard so the content \
    editor can add metadata via a form as part of the import process.

    """

    def __init__(self, sourcefile=None, post_data=None, ignore_unknown_headers=False,
                 ignore_invalid_rows=False, dataset_meta_in_filename=False):

        self.sourcefile = sourcefile
        self.post_data = post_data
        self.ignore_unknown_headers = ignore_unknown_headers
        self.ignore_invalid_rows = ignore_invalid_rows
        self.dataset_meta_in_filename = dataset_meta_in_filename

        if sourcefile:
            self.extract()

    def extract(self):
        """Create a valid dataset from data in the sourcefile.

        We create a dataset object.

        We clean up the headers.

        We email ourselves if the source file cannot be converted \
        to a datset, and we save that sourcefile in a tempoary \
        location, as well as emailing it, for analysis.

        """
        self._extract_meta()

        data_stream = self.sourcefile.read()
        self.data = self.get_data(data_stream)

        return self

    def validate(self):
        """
        Runs validation on the extracted data using the parser's
        validation.
        """
        return self.parser.validate(self.data)

    def save(self):
        """
        Delegates to the parser's save method.
        """
        return self.parser.save()

    def deferred(self):
        """
        Gets a deferred object from the parser, adding to it
        the parser's class key.

        Returns the deferred object which can be later serialized
        and sent to queue, for later resolving it.
        """
        deferred = self.parser.deferred()
        deferred['class'] = get_parser_key(self.parser.__class__)

        return deferred

    def resolve(self, deferred):
        """
        Takes a deferred importer object which sets the appropriate
        parser and delegates to it's resolve method.
        """
        # get the parser class key
        klass = deferred['class']

        if not klass:
            raise Exception('Deferred object missing class key: %s' % klass)

        # get the parser class and resolve the deferred object
        self.parser = get_parser(klass).resolve(deferred)
        # return self for fluency's sake
        return self

    def get_data(self, stream):
        """
        Takes a data stream read from the source file, extracts a
        dataset from it and stores it in `self.data`.
        """
        raise NotImplementedError()

    def normalize_headers(self, headers):
        """Clean the headers of the dataset.

        We replace the existing headers with new ones that \
        have been cleaned and normalized.

        To clean, we strip white space and common joining \
        symbols, and we convert all to lowercase.

        To normalize, we match the header to strings in a \
        string scope map, and convert to the string in the \
        map when our key is either the string or in the scope \
        list.

        """
        symbols = {
            ord('_'): None,
            ord('-'): None,
            ord('"'): None,
            ord(' '): None,
            ord("'"): None,
        }
        scopes_map = self._get_header_scopes()
        normalized_headers = []

        for index, header in enumerate(headers):

            tmp = unicode(header).translate(symbols).lower()

            for k, v in scopes_map.iteritems():

                if tmp == k or tmp in v:
                    normalized_headers[index] = k

        return normalized_headers

    def import_error(self):
        """
        Handle import exceptions by sending an email to admins
        with the file attached.
        """
        #TODO: need to attach the file to the sent email
        dt = datetime.now().isoformat()

        this_file = TEMP_FILES_DIR + \
            '/failed_import_{timestamp}_{filename}'.format(
                timestamp=dt,
                filename=unicode(self.sourcefile)
            )

        with open(this_file, 'wb+') as tmp_file:
            for chunk in self.sourcefile.chunks():
                tmp_file.write(chunk)

        # email ourselves that we have a file to check
        subject = 'Open Budget: Failed File Import'
        message = 'The file is attached.'
        sender = EMAIL_HOST_USER
        recipients = [ADMINS]

        send_mail(subject, message, sender, recipients)

    def _extract_meta(self):
        """Get's the meta data for the dataset. \
        The meta data determines the parser class to be used for \
        parsing and saving the data, and the data for creating the \
        container object.

        Each file that is imported has rows of data, where each row \
        is, ultimately, some object. The objects contained in the \
        file also need additional data in order to be contextualized \
        in the datastore.

        For example, if the sourcefile is full of entries that are \
        nodes in a template, we still need to know, for example the \
        name of the template, the entity it belongs to, and so on.

        When data is imported via an interactive wizard, this \
        "metadata" can be filled out in a form by the person doing \
        the import.

        Alternatively, the BaseImporter class also supports parsing \
        the filename of the sourcefile to extract the required \
        metadata. For this option, dataset_meta_in_filename must be \
        True. Importing like this is handy during development, \
        but you'll need to know that your dataset is valid in \
        advance, as there will be no interactive wizard to fix data.

        """
        if self.dataset_meta_in_filename:
            parser = self._get_parser_from_filename()
        else:
            parser = self._get_parser_from_post()

        self.parser = parser

        return self

    def _get_header_scopes(self):
        """
        Gets the available strings and scopes which are used
        for normalizing the headers.
        """

        scopes_map = {}

        strings = String.objects.filter(parent__isnull=True)

        for string in strings:
            scopes_map[string.string] = [scope.string for scope in string.scope_set.all()]

        return scopes_map

    def _get_parser_from_filename(self):
        """Extract necessary info on the dataset from the filename.

        FILENAME FORMAT:
        |PARSER|_|CONTAINEROBJECT-ATTRS|.extension

        Arguments for object attributes are keywords.
        For object attributes, each attribute is separated by a \
        semi-colon. Multiple values for an attribute (i.e: m2m), \
        are comma separated.

        EXAMPLE - BUDGET TEMPLATE:
        budgettemplate_name=israel-municipality;divisions=4,5,6;period_start=2001-01-10.csv

        EXAMPLE - BUDGET OR ACTUAL:
        budget_entity=1,period_start=2001-01-01;period_end=2001-12-31.csv

        """

        # an empty dict to populate with data for our container object
        container_object_dict = {}

        # get our data string from the filename
        keys, ext = os.path.splitext(unicode(self.sourcefile))

        # first, split the parser key from the container_object keys
        parser_key, attributes_str = keys.split('_', 1)

        # get the appropriate parser class
        parser = get_parser(parser_key)

        # now get the keyword arguments for the container object
        container_object_kwargs = attributes_str.split(';')

        # and split these keyword arguments into keys and values
        for kwarg in container_object_kwargs:
            attr_key, attr_val = kwarg.split('=')

            # and make sure each attribute is valid for the container model
            try:
                getattr(parser.container_model, attr_key)
            except AttributeError as e:
                raise e

            # if the value has commas, it is an m2m related field
            if ',' in attr_val:
                attr_val = tuple(attr_val.split(','))

            container_object_dict[attr_key] = attr_val

        # return instantiated parser
        return parser(container_object_dict)

    def _get_parser_from_post(self):
        """Extract necessary info on the dataset from the request's POST data.

        For now relies on the same format of the above file name meta extractor, \
        except it looks for the parser type under the key `type` and for the rest \
        under the key `attributes`.
        """
        #TODO: refactor the meta extraction from string parsing to proper data in POST
        container_object_dict = {}
        parser_key = self.post_data.get('type', 'budget')
        attributes_str = self.post_data.get('attributes', None)

        # get the appropriate parser class
        parser = get_parser(parser_key)

        if attributes_str:
            # parse the attributes
            # split the string to pairs
            attributes = attributes_str.split(';')
            for attr in attributes:
                # split each pair to key-value
                attr_key, attr_val = attr.split('=')

                # check that this key belongs to our parser's container model
                try:
                    getattr(parser.container_model, attr_key)
                except AttributeError as e:
                    try:
                        # if it's not an attribute of the container model's class
                        # it might be an attribute of its instance (because of use of mixins)
                        getattr(parser.container_model(), attr_key)
                    except AttributeError as e:
                        raise e

                # if the value has commas, it is an m2m related field
                if ',' in attr_val:
                    attr_val = tuple(attr_val.split(','))

                container_object_dict[attr_key] = attr_val

            # return instantiated parser
            return parser(container_object_dict)

        else:
            raise Exception('No attributes given in meta data.')
