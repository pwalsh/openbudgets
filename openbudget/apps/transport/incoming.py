import os
import datetime
import tablib
from operator import itemgetter
from openbudget.settings.base import TEMP_FILES_DIR, ADMINS
from openbudget.apps.transport.models import String
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode, BudgetTemplateNodeRelation, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.entities.models import Entity, Domain,DomainDivision


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

    def __init__(
        self,
        sourcefile,
        ignore_unknown_headers=False,
        ignore_invalid_rows=False,
        dataset_meta_in_filename=False
    ):
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
        except AttributeError, e:
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
        response = {
            'valid': False
        }

        #valid_structure = self._valid_data_structure(dataset)
        #valid_values = self._valid_data_values(dataset)

        # TODO: temporary True until I write this function!!!
        response['valid'] = True
        value = response
        return response

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
        objs = dataset.dict

        print 'BEFORE SORT'
        for obj in objs:
            print obj['code'], obj['parent'], obj['inverse']
        # TODO: The best impl would be to sort this list
        # so that relational dependencies (eg: parent, inverse)
        # are always commited before they are needed.
        # The itemgetter sorting below was part of an attempt at this
        # but it is ultimately flawed, as it is only sorting based on
        # the characters in the string. Leaving it here for now as
        # a reminder.
        #
        # If the list was sorted properly, in the section below,
        # we would not need to iterate over the list twice to commit.
        # As it is, this only currently works because the related
        # fields are not required fields. On the other hand, because
        # of the current implementation, we can use bulk_create on the
        # iterations. I haven't consider what this means in
        # performance, but the fact is that it is currently not
        # generic enough for *required* related fields, should
        # that use case arise.
        #objs.sort(key=itemgetter('inverse'))
        #objs.sort(key=itemgetter('parent'))


        non_dependent_list = []
        parent_dependent_list = []
        inverse_dependent_list = []

        for index, item in enumerate(objs):

            if not item['parent'] and not item['inverse']:
                non_dependent_list.append(item)

            if item['parent']:
                #for row in objs:
                #    if (row['code'] == item['parent']):
                parent_dependent_list.append(item)

            if item['inverse']:
                #for row in objs:
                #    if (row['code'] == item['parent']):
                inverse_dependent_list.append(item)

            for index, thing in enumerate(parent_dependent_list):
                if thing['code'] == item['parent']:
                    objs.pop(index)
                    objs.append(thing)

        print 'AFTER SORT'
        for obj in objs:
            print obj['code'], obj['parent'], obj['inverse']

        print 'NON DEPENDENT LIST'
        for obj in non_dependent_list:
            print obj['code']
        print 'PARENT DEPENDENT LIST'
        for obj in parent_dependent_list:
            print obj['code']
        print 'INVERSE DEPENDENT LIST'
        for obj in inverse_dependent_list:
            print obj['code']


        # budget template nodes, first pass: commit basic object
        for obj in objs:
            child_model = modelset['items'].objects.create(
                code=obj['code'],
                name=obj['name'],
                direction=obj['direction'],
            )
            BudgetTemplateNodeRelation.objects.create(
                template=container_model,
                node=child_model
            )

        # budget template nodes, 2nd pass: add parents
        for obj in objs:
            if obj['parent']:
                if obj['parentscope']:
                    parentscope = BudgetTemplateNode.objects.get(
                        code=obj['parentscope'],
                        templates__in=[container_model]
                    )
                    parent = BudgetTemplateNode.objects.get(
                        code=obj['parent'],
                        parent=parentscope,
                        templates__in=[container_model]
                    )
                else:
                    parent = BudgetTemplateNode.objects.get(
                        code=obj['parent'],
                        parent__isnull=True,
                        templates__in=[container_model]
                    )
                this_obj = BudgetTemplateNode.objects.get(
                    code=obj['code'],
                    templates__in=[container_model]
                )
                this_obj.parent = parent
                this_obj.save()

        # budget template nodes, 3rd pass: add inverse relations
        for obj in objs:
            if obj['inverse']:
                if ',' in obj['inverse']:
                    inverses = obj['inverse'].split(',')
                    inversescopes = obj['inversescope'].split(',')
                else:
                    inverses = [obj['inverse']]
                    inversescopes = [obj['inversescope']]

                for i, inverse in enumerate(inverses):
                    if inversescopes[i]:
                        iscope = BudgetTemplateNode.objects.get(
                            code=inversescopes[i],
                            templates__in=[container_model]
                        )
                        i = BudgetTemplateNode.objects.get(
                            code=inverse,
                            parent=iscope,
                            templates__in=[container_model]
                        )
                    else:
                        i = BudgetTemplateNode.objects.get(
                            code=inverse,
                            parent__isnull=True,
                            templates__in=[container_model]
                        )

                    this_obj = BudgetTemplateNode.objects.get(code=obj['code'], templates__in=[container_model])
                    this_obj.inverse.add(i)

        self._save_sourcefile()
        value = True
        return value

    def _valid_data_structure(self, dataset):
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

    def _valid_data_values(self, dataset):
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
        except AttributeError, e:
            raise e
        # now get the keyword arguments for the container object
        containerobject_kwargs = tmp.split(';')
        # and split this keyword arguements into attributes and values
        for kwarg in containerobject_kwargs:
            attr, v = kwarg.split('=')
            # and make sure each attribute is valid for the container
            try:
                getattr(modelset['container'], attr)
            except AttributeError, e:
                raise e
            # if the value has commas, it is an m2m related field
            if ',' in v:
                v = tuple(v.split(','))
            containerobject_dict[attr] = v
        value = (modelset, containerobject_dict)
        return value

    def _get_meta_from_post(self):
        # TODO: When we have an interactive importer
        value - None
        return value
