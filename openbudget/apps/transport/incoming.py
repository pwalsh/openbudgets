import os
import datetime
import tablib
from django.core.mail import send_mail
from openbudget.settings.base import TEMP_FILES_DIR, ADMINS, EMAIL_HOST_USER
from openbudget.apps.transport.models import String
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode,\
    BudgetTemplateNodeRelation, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.entities.models import Entity, DomainDivision


class DataImporter(object):
    """Gets data out of files and into the database.

    This class can handle any of the supported datasets for importing.

    At this stage, that means Budget Templates (template and related
    node objects), and Budgets/Actuals (Budget or Actual, and related
    items).

    The importer supports a lower level import by parsing the
    file name for meta data - useful while testing, so developers do
    not have to work with an interactive importer. Otherwise, \
    it should be used with an interactive wizard so the content \
    editor can add netadata via a form as part of the import process.

    """

    def __init__(self, sourcefile, ignore_unknown_headers=False,
                 ignore_invalid_rows=False, dataset_meta_in_filename=False):
        self.sourcefile = sourcefile
        self.ignore_unknown_headers = ignore_unknown_headers
        self.ignore_invalid_rows = ignore_invalid_rows
        self.dataset_meta_in_filename = dataset_meta_in_filename
        self.modelsets = {
            'budgettemplate': {
                'container': BudgetTemplate,
                'items': BudgetTemplateNode,
                'container_relation': DomainDivision
            },
            'budget': {
                'container': Budget,
                'items': BudgetItem,
                'container_relation': Entity
            },
            'actual': {
                'container': Actual,
                'items': ActualItem,
                'container_relation': Entity
            },
        }

    def dataset_meta(self):
        """Get's the meta data for the dataset.

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
            value = self._get_meta_from_filename()
        else:
            value = self._get_meta_from_post()
        return value

    def dataset(self):
        """Create a valid dataset from data in the sourcefile.

        We create a tablib.Dataset object.

        We clean up the headers.

        We email ourselves if the source file cannot be converted \
        to a datset, and we save that sourcefile in a tempoary \
        location, as well as emailing it, for analysis.

        """
        value = None
        datastream = self.sourcefile.read()

        try:
            raw_dataset = tablib.import_set(datastream)
        except AttributeError as e:
            # TODO: need to get more specific exception
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
            raise e

        dataset = self._normalize_headers(raw_dataset)
        value = dataset

        return value

    def validate(self, dataset):
        response = {'valid': False}

        #valid_structure = self._validate_data_structure(dataset)
        #valid_values = self._validate_data_values(dataset)

        # TODO: temporary True until I write this function!!!
        response['valid'] = True
        value = response
        return value

    def save(self, dataset):
        """Save all the objects from this import"""

        value = False

        # get the dataset's meta data:
        # i.e: that which is not in rows and columns
        modelset, containerobject_dict = self.dataset_meta()

        # now we create the container model
        # TODO: This can be worked on to make it more generic
        class_name = modelset['container'].get_class_name()

        if class_name == 'budgettemplate':
            container_model = modelset['container'].objects.create(
                name=containerobject_dict['name'],
            )
            for division in containerobject_dict['divisions']:
                container_model.divisions.add(division)

        elif class_name == 'budget' or class_name == 'actual':
            entity = Entity.objects.get(
                pk=containerobject_dict['entity']
            )
            container_model = modelset['container'].objects.create(
                entity=entity,
                period_start=containerobject_dict['period_start'],
                period_end=containerobject_dict['period_end'],
            )

        else:
            return 'bork... we cant deal with this thing man.'

        # now we process all objects in the dataset
        saved_cache = {}

        def _generate_lookup(objects):
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
                    key = '%s:%s' % (code, obj['parent'])
                    # see if `parent` is also in conflict by looking for a `parentalias`
                    if 'parentalias' in obj and obj['parentalias']:
                        key = key + ':' + obj['parentalias']

                    if key in lookup_table:
                        raise Exception

                    lookup_table[key] = obj

        objects_lookup = _generate_lookup(dataset.dict)

        def _lookup_object(code=None, parent='', alias=''):
            if code:
                key = ''
                if code in objects_lookup:
                    key = code
                elif parent or alias:
                    if not parent:
                        parent = alias.split(':')[0]
                    key = ':'.join((code, parent))
                    if key not in objects_lookup:
                        key = ':'.join((code, alias))

                if key in objects_lookup:
                    return key, objects_lookup[key]

            return None, None

        def _save_object(obj, key):
            inverses = []
            # check if we already saved this object and have it in cache
            if key in saved_cache:
                return saved_cache[key]

            if 'inverse' in obj:
                inverse_codes = obj['inverse'].split(',')

                if len(inverse_codes):
                    aliases = []

                    if 'inversealias' in obj:
                        aliases = obj['inversealias'].split(',')
                        # clean up
                        del obj['inversealias']

                    for i, inv_code in enumerate(inverse_codes):
                        if i in aliases:
                            inverse_key, inverse = _lookup_object(code=inv_code, alias=aliases[i])
                        else:
                            inverse_key, inverse = _lookup_object(code=inv_code)

                        if inverse_key in saved_cache:
                            inverses.append(saved_cache[inverse_key])
                        else:
                            inverses.append(_save_object(inverse, inverse_key))

                else:
                    # clean inverse
                    if 'inversealias' in obj:
                        del obj['inversealias']

                del obj['inverse']

            if 'parent' in obj and obj['parent']:

                if 'parentalias' in obj:
                    alias = obj['parentalias']
                    # clean parentalias
                    del obj['parentalias']
                else:
                    alias = ''

                parent_key, parent = _lookup_object(code=obj['parent'], alias=alias)

                if parent_key in saved_cache:
                    obj['parent'] = saved_cache[parent_key]
                else:
                    parent = _save_object(parent, parent_key)
                    obj['parent'] = parent

            elif 'parent' in obj:
                # clean parent
                del obj['parent']

                if 'parentalias' in obj:
                    # clean parentalias
                    del obj['parentalias']

            item = modelset['items'].objects.create(**obj)

            if len(inverses):
                for inverse in inverses:
                    item.inverse.add(inverse)

            # cache the saved object
            saved_cache[key] = item

            BudgetTemplateNodeRelation.objects.create(
                template=container_model,
                node=item
            )

            return item

        for key, obj in objects_lookup.iteritems():
            _save_object(obj, key)

        self._save_sourcefile()
        return True

    def __detect_relational_ambiguities(self):
        objects = self.dataset.dict
        available_codes = [o['code'] for o in objects]

        for obj in objects:
            parent = obj['parent']
            inverse = obj['inverse']

            if parent:
                if parent not in available_codes:
                    raise ImportError
                if available_codes.count(parent) > 1:
                    raise ImportError

            if inverse:
                if inverse not in available_codes:
                    raise ImportError
                if available_codes.count(inverse) > 1:
                    raise ImportError

    def _validate_data_structure(self, dataset):
        """Validate the data structure against a template"""
        # get template
        # validate headers
        # validate nodes
        # return tuple of (bool, list(co-ordinates))
        # the list will match the bool value, so if it is false
        # a list of false co-ordinates, and if true, a list of true
        # presuming i can use the list of tru in subsequent function
        # need to see if that is so
        pass

    def _validate_data_values(self, dataset):
        """Validate that the data values match the expected input"""
        # check type matches expected
        # return tuple of (bool, list(co-ordinates))
        # the list will match the bool value, so if it is false
        # a list of false co-ordinates, and if true, a list of true
        # presuming i can use the list of tru in subsequent function
        # need to see if that is so
        pass

    def _save_sourcefile(self):
        """Saves an uploaded source file"""
        value = False

        # do stuff

        value = True
        return value

    def _normalize_headers(self, dataset):
        """Clean the headers of the dataset.

        We replace the existing headers with new ones that \
        have been cleaned and normalized.

        To clean, we strip white space and common joining \
        symbols, and we convert all to lowercase.

        To normalize, we match the header to strings in a \
        string alias map, and convert to the string in the \
        map when our key is either the string or in the alias \
        list.

        """
        symbols = {
            ord('_'): None,
            ord('-'): None,
            ord('"'): None,
            ord(' '): None,
            ord("'"): None,
        }
        for index, header in enumerate(dataset.headers):
            tmp = unicode(header).translate(symbols).lower()
            alias_map = self._get_header_aliases()
            for k, v in alias_map.iteritems():
                if (tmp == k) or (tmp in v):
                    new_header = k
                    dataset.headers[index] = new_header
        value = dataset
        return value

    def _get_header_aliases(self):
        """Hit the DB and get the available strings and aliases."""
        value = {}
        strings = String.objects.filter(parent__isnull=True)
        for string in strings:
           value[string.string] = [alias.string for alias in string.alias_set.all()]
        return value

    def _get_meta_from_filename(self):
        """Extract necessary info on the dataset from the filename.

        FILENAME FORMAT:
        |MODELSET|_|CONTAINEROBJECT-ATTRS|.extension

        Arguments for object attributes are keywords.
        For object attributes, each attribute is separated by a \
        semi-colon. Multiple values for an attribute (i.e: m2m), \
        are comma separated.

        EXAMPLE - BUDGET TEMPLATE:
        budgettemplate_name=israel-municipality;divisions=4,5,6.csv

        EXAMPLE - BUDGET OR ACTUAL:
        budget_entity=1,period_start=2001-01-01;period_end=2001-12-31.csv

        """

        value = None
        # an empty dict to populate with data for our container object
        containerobject_dict = {}
        # get our data string from the filename
        keys, ext = os.path.splitext(unicode(self.sourcefile))
        # first, split the modelset key from the containerobject keys
        modelset_key, tmp = keys.split('_')
        # check the modelset key is valid, otherwise we'll stop here
        try:
            modelset = self.modelsets[modelset_key]
        except AttributeError as e:
            raise e
        # now get the keyword arguments for the container object
        containerobject_kwargs = tmp.split(';')
        # and split this keyword arguements into attributes and values
        for kwarg in containerobject_kwargs:
            attr, v = kwarg.split('=')
            # and make sure each attribute is valid for the container
            try:
                getattr(modelset['container'], attr)
            except AttributeError as e:
                raise e
            # if the value has commas, it is an m2m related field
            if ',' in v:
                v = tuple(v.split(','))
            containerobject_dict[attr] = v
        value = (modelset, containerobject_dict)
        return value

    def _get_meta_from_post(self):
        # TODO: When we have an interactive importer
        value = None
        return value
