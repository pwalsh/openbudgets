import os
from openbudget.apps.transport.models import String
from openbudget.apps.transport.incoming.parsers import get_parser, get_parser_key


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
        return self.parser.validate(self.data)

    def save(self):
        return self.parser.save()

    def deferred(self):
        deferred = self.parser.deferred()
        deferred['class'] = get_parser_key(self.parser.__class__)

        return deferred

    def resolve(self, deferred):
        klass = deferred['class']

        if not klass:
            raise Exception('Deferred object missing class key: %s' % klass)

        self.parser = get_parser(klass).resolve(deferred)
        return self

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
