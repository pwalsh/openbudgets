import os
import datetime
import tablib
from django.core.mail import send_mail
from openbudget.settings.base import TEMP_FILES_DIR, ADMINS, EMAIL_HOST_USER
from openbudget.apps.transport.models import String
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode,\
    BudgetTemplateNodeRelation, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.entities.models import Entity, DomainDivision


class BaseParser(object):

    def __init__(self, container_object_dict):
        self.container_object_dict = container_object_dict

    ROUTE_SEPARATOR = '|'
    ITEM_SEPARATOR = ';'
    saved_cache = {}
    objects_lookup = {}

    def validate(self, data):
        self._generate_lookup(data)
        return True

    def save(self):

        self._create_container()

        for key, obj in self.objects_lookup.iteritems():
            self._save_object(obj, key)

        return True


class BudgetTemplateParser(BaseParser):

    container_model = BudgetTemplate
    item_model = BudgetTemplateNode

    def _save_object(self, obj, key):
        inverses = []
        # check if we already saved this object and have it in cache
        if key in self.saved_cache:
            return self.saved_cache[key]

        if 'inverse' in obj:
            inverse_codes = obj['inverse'].split(self.ITEM_SEPARATOR)

            if len(inverse_codes) and inverse_codes[0]:
                scopes = []

                if 'inversescope' in obj:
                    scopes = obj['inversescope'].split(self.ITEM_SEPARATOR)
                    # clean up
                    del obj['inversescope']

                for i, inv_code in enumerate(inverse_codes):
                    if i in scopes:
                        inverse_key, inverse = self._lookup_object(code=inv_code, scope=scopes[i])
                    else:
                        inverse_key, inverse = self._lookup_object(code=inv_code)

                    if not inverse_key or not inverse:
                        raise Exception('Could not locate an inverse, \
                                        probably you have a syntax error: inverse = %s' % obj['inverse'])

                    if inverse_key in self.saved_cache:
                        inverses.append(self.saved_cache[inverse_key])
                    else:
                        inverses.append(self._save_object(inverse, inverse_key))

            else:
                # clean inverse
                if 'inversescope' in obj:
                    del obj['inversescope']

            del obj['inverse']

        if 'parent' in obj and obj['parent']:

            if 'parentscope' in obj:
                scope = obj['parentscope']
                # clean parentscope
                del obj['parentscope']
            else:
                scope = ''

            parent_key, parent = self._lookup_object(code=obj['parent'], scope=scope)

            if parent_key in self.saved_cache:
                obj['parent'] = self.saved_cache[parent_key]
            else:
                parent = self._save_object(parent, parent_key)
                obj['parent'] = parent

        elif 'parent' in obj:
            # clean parent
            del obj['parent']

            if 'parentscope' in obj:
                # clean parentscope
                del obj['parentscope']

        item = self.item_model.objects.create(**obj)

        if len(inverses):
            for inverse in inverses:
                item.inverse.add(inverse)

        # cache the saved object
        self.saved_cache[key] = item

        BudgetTemplateNodeRelation.objects.create(
            template=self.container_object,
            node=item
        )

        return item

    def _create_container(self):

        container = self.container_model.objects.create(
            name=self.container_object_dict['name'],
        )

        for division in self.container_object_dict['divisions']:
            container.divisions.add(division)

        self.container_object = container

    def _generate_lookup(self, objects):
        conflicting = {}
        lookup_table = {}

        for obj in objects:
            code = obj['code']

            if code in lookup_table:
                if code not in conflicting:
                    conflicting[code] = []
                conflicting[code].append(obj)
            else:
                lookup_table[code] = obj

        for code, obj_list in conflicting.iteritems():
            conflicting[code].append(lookup_table.pop(code))

        for code, obj_list in conflicting.iteritems():
            for obj in obj_list:
                # assuming there can't be two top level nodes with same code, naturally
                key = self.ROUTE_SEPARATOR.join((code, obj['parent']))
                # see if `parent` is also in conflict by looking for a `parentscope`
                if 'parentscope' in obj and obj['parentscope']:
                    key = key + self.ROUTE_SEPARATOR + obj['parentscope']

                if key in lookup_table:
                    raise Exception('Found key: %s of object: %s colliding with: %s' % (key, obj, lookup_table[key]))

                lookup_table[key] = obj

        self.objects_lookup = lookup_table

    def _lookup_object(self, code=None, parent='', scope=''):
        if code:

            key = ''

            if code in self.objects_lookup:
                key = code

            elif parent or scope:

                if not parent:
                    parent = scope.split(self.ROUTE_SEPARATOR)[0]

                key = self.ROUTE_SEPARATOR.join((code, parent))

                if key not in self.objects_lookup:
                    key = self.ROUTE_SEPARATOR.join((code, scope))

            if key in self.objects_lookup:
                return key, self.objects_lookup[key]

        return None, None


class BudgetParser(BaseParser):

    container_model = Budget
    item_model = BudgetItem

    def _create_container(self):

        entity = Entity.objects.get(
            pk=self.container_object_dict['entity']
        )

        self.container_object = self.container_model.objects.create(
            entity=entity,
            period_start=self.container_object_dict['period_start'],
            period_end=self.container_object_dict['period_end'],
        )


class ActualParser(BudgetParser):

    container_model = Actual
    item_model = ActualItem


PARSERS_MAP = {
    'budgettemplate': BudgetTemplateParser,
    'budget': BudgetParser,
    'actual': ActualParser
}


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

    def __init__(self, sourcefile, post_data, ignore_unknown_headers=False,
                 ignore_invalid_rows=False, dataset_meta_in_filename=False):

        self.sourcefile = sourcefile
        self.post_data = post_data
        self.ignore_unknown_headers = ignore_unknown_headers
        self.ignore_invalid_rows = ignore_invalid_rows
        self.dataset_meta_in_filename = dataset_meta_in_filename

        self.extract()

    def extract_meta(self):
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

    def extract(self):
        """Create a valid dataset from data in the sourcefile.

        We create a tablib.Dataset object.

        We clean up the headers.

        We email ourselves if the source file cannot be converted \
        to a datset, and we save that sourcefile in a tempoary \
        location, as well as emailing it, for analysis.

        """
        self.extract_meta()

        data_stream = self.sourcefile.read()
        self.data = self.get_data(data_stream)

        return self

    def validate(self):
        self.parser.validate(self.data)
        return True

    def save(self):
        self.parser.save()
        return True

    def get_data(self, stream):
        raise NotImplementedError()

    def _get_header_scopes(self):
        """
        Hit the DB and get the available strings and scopes.
        """

        value = {}

        strings = String.objects.filter(parent__isnull=True)

        for string in strings:
            value[string.string] = [scope.string for scope in string.scope_set.all()]

        return value

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

        for index, header in enumerate(dataset.headers):

            tmp = unicode(header).translate(symbols).lower()
            scope_map = self._get_header_scopes()

            for k, v in scope_map.iteritems():

                if (tmp == k) or (tmp in v):

                    new_header = k
                    dataset.headers[index] = new_header

        return dataset

    def _import_error(self):
        """
        Handle import exception raised by calling `tablib.import_set`
        """

        dt = datetime.datetime.now().isoformat()

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
