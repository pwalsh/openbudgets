import os
from datetime import datetime
import tablib
from django.core.mail import send_mail
from openbudget.settings.base import TEMP_FILES_DIR, ADMINS, EMAIL_HOST_USER
from openbudget.apps.transport.models import String
from openbudget.apps.transport.incoming.parsers import PARSERS_MAP


class BaseImporter(object):
    """Gets data out of files and into the database.

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

        We create a tablib.Dataset object.

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
        return self.parser.validate(self.data)

    def save(self):
        self.parser.save()
        return True

    def deferred(self):
        deferred = self.parser.deferred()

        parser_key = ''
        for key, parser_class in PARSERS_MAP.iteritems():
            if self.parser.__class__ is parser_class:
                parser_key = key
                break

        deferred['parser'] = parser_key

        return deferred

    def resolve(self, deferred):
        parser_key = deferred['parser']
        container_dict = deferred['container']

        if not parser_key or not container_dict:
            raise Exception('Bad deferred object: %s, %s' % (parser_key, container_dict))

        self.parser = PARSERS_MAP[parser_key](container_dict)
        self.parser.objects_lookup = deferred['items']
        return self.save()

    def get_data(self, stream):
        raise NotImplementedError()

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

        Alternatively, the DataImporter class also supports parsing \
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
        Hit the DB and get the available strings and scopes.
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
        budgettemplate_name=israel-municipality;divisions=4,5,6.csv

        EXAMPLE - BUDGET OR ACTUAL:
        budget_entity=1,period_start=2001-01-01;period_end=2001-12-31.csv

        """

        # an empty dict to populate with data for our container object
        container_object_dict = {}

        # get our data string from the filename
        keys, ext = os.path.splitext(unicode(self.sourcefile))

        # first, split the parser key from the container_object keys
        parser_key, tmp = keys.split('_')

        # check the parser key is valid, otherwise we'll stop here
        try:
            parser = PARSERS_MAP[parser_key]
        except AttributeError as e:
            raise e

        # now get the keyword arguments for the container object
        container_object_kwargs = tmp.split(';')

        # and split this keyword arguments into attributes and values
        for kwarg in container_object_kwargs:
            attr, val = kwarg.split('=')

            # and make sure each attribute is valid for the container model
            try:
                getattr(parser.container_model, attr)
            except AttributeError as e:
                raise e

            # if the value has commas, it is an m2m related field
            if ',' in val:
                val = tuple(val.split(','))

            container_object_dict[attr] = val

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
        attributes = self.post_data.get('attributes', None)

        try:
            parser = PARSERS_MAP[parser_key]
        except AttributeError as e:
            raise e

        if attributes:
            attributes = attributes.split(';')
            for attr in attributes:
                key, val = attr.split('=')

                try:
                    getattr(parser.container_model, key)
                except AttributeError as e:
                    try:
                        getattr(parser.container_model(), key)
                    except AttributeError as e:
                        raise e

                # if the value has commas, it is an m2m related field
                if ',' in val:
                    val = tuple(val.split(','))

                container_object_dict[key] = val

        # return instantiated parser
        return parser(container_object_dict)


class TablibImporter(BaseImporter):

    def get_data(self, stream):
        try:
            raw_dataset = tablib.import_set(stream)
        except AttributeError as e:
            # TODO: need to get more specific exception
            self._import_error()
            raise e

        # `_normalize_headers` may transform the headers and returns the same data object
        # we then return the dict view of the data
        return self._normalize_headers(raw_dataset).dict

    def _normalize_headers(self, dataset):
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
        #TODO: see if this method can be moved to the BaseImporter in a more generic way
        symbols = {
            ord('_'): None,
            ord('-'): None,
            ord('"'): None,
            ord(' '): None,
            ord("'"): None,
        }
        scopes_map = self._get_header_scopes()

        for index, header in enumerate(dataset.headers):

            tmp = unicode(header).translate(symbols).lower()

            for k, v in scopes_map.iteritems():

                if tmp == k or tmp in v:
                    dataset.headers[index] = k

        return dataset

    def _import_error(self):
        """
        Handle import exception raised by calling `tablib.import_set`
        """

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
