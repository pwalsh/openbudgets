import datetime
import tablib
from openbudget.settings.base import TEMP_FILES_DIR, ADMINS
from openbudget.apps.transport.models import String
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.entities.models import Entity, Domain,DomainDivision


class FileImporter(object):
    """Gets data out of files and into the database."""

    def __init__(self, sourcefile, datatype=None, nesting_style=None):
        self.sourcefile = sourcefile
        self.data_type = datatype
        self.nesting_style = nesting_style
        self.datatypes = {
            'budgettemplate': (
                BudgetTemplate,
                DomainDivision,
                BudgetTemplateNode
            ),
            'budget': (
                Budget,
                Entity,
                BudgetItem
            ),
            'actual': (
                Actual,
                Entity,
                ActualItem
            ),
        }

    def get_metadata(self):
        """Get metadata from file by convention.

        Allows us to import data without an interactive wizard.

        format: NAME-OF-OBJECT_DATATYPE_DIVISIONS_TUPLE.extension
        example: budgettemplate_israel-municipality_4,5,6.csv
        """
        keys = unicode(self.sourcefile).split('.')[0].split('_')
        # divisions is budget template specific at this stage
        datatype, name, divisions = keys[0], keys[1], \
        tuple(keys[2].split(','))
        value = (datatype, name, divisions)
        return value

    def create_dataset(self):
        """Turn the datastream into a dataset object"""
        datastream = self.sourcefile.read()

        try:
            dataset = tablib.import_set(datastream)
            value = dataset

        except Exception, e:
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

            value = 'FAILED'

        return value

    def persist_sourcefile(self):
        """Saves an uploaded source file to a work directory."""
        pass

    def normalize_headers(self, dataset):
        """Clean the headers of the dataframe.

        We replace the existing headers with new ones that have
        been cleaned and normalized.

        To clean, we strip white space and common joining symbols,
        and we convert all to lowercase.
        To normalize, we match the header to strings in a string
        alias map, and convert to the string in the map when our
        key is either the string or in the alias list.

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

    def validate_data_structure(self, dataset):
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

    def validate_data_values(self, dataset):
        """Validate that the data values match the expected input"""
        # check type matches expected
        # return tuple of (bool, list(co-ordinates))
        # the list will match the bool value, so if it is false
        # a list of false co-ordinates, and if true, a list of true
        # presuming i can use the list of tru in subsequent function
        # need to see if that is so
        pass

    def to_db(self, dataset):
        """Save a dataset to the database"""
        if self.nesting_style:
            # parse parent child relations according to rules of style
            pass

        # get the right models from the metadata datatype
        models = self.datatypes[self.get_metadata()[0]]

        # relations of the head model:
        # if list, is m2m, if int, is fk.
        relations = self.get_metadata()[2]

        head_model = models[0].objects.create(
            name=self.get_metadata()[1]
        )

        # this code still expects a list...
        for obj_id in self.get_metadata()[2]:
            relation_model = models[1].objects.get(id=obj_id)
            head_model.divisions.add(relation_model)

        # now we process all our objects
        # we build them in a certain order to make sure
        # related objects exist before we need them
        nodes = dataset.dict

        nodes_with_inverse = [node for node in nodes if \
        node['inverse']]

        nodes_without_inverse = [node for node in nodes if \
        not node['inverse']]

        parent_nodes_with_inverse = [node for node in \
        nodes_with_inverse if not node['parent']]

        parent_nodes_without_inverse = [node for node in \
        nodes_without_inverse if not node['parent']]

        child_nodes_with_inverse = [node for node in \
        nodes_with_inverse if node['parent']]

        child_nodes_without_inverse = [node for node in \
        nodes_without_inverse if node['parent']]


        for obj in parent_nodes_without_inverse:

            if obj['direction'] == 'REVENUE':
                direction = 1
            elif obj['direction'] == 'EXPENDITURE':
                direction = 2

            child_model = models[2].objects.create(
                template=head_model,
                code=obj['code'],
                name=obj['name'],
                direction=direction,
            )

        for obj in parent_nodes_with_inverse:

            if obj['direction'] == 'REVENUE':
                direction = 1
            elif obj['direction'] == 'EXPENDITURE':
                direction = 2

            print 'about to inverse'
            print obj['code']
            print obj['inverse']
            inverse_relation = models[2].objects.get(
                code=obj['inverse']
            )

            child_model = models[2].objects.create(
                template=head_model,
                code=obj['code'],
                name=obj['name'],
                direction=direction
            )

            child_model.inverse.add(inverse_relation)

        for obj in child_nodes_without_inverse:

            if obj['direction'] == 'REVENUE':
                direction = 1
            elif obj['direction'] == 'EXPENDITURE':
                direction = 2

            parent_relation = models[2].objects.get(
                code=obj['parent']
            )

            child_model = models[2].objects.create(
                template=head_model,
                code=obj['code'],
                name=obj['name'],
                direction=direction,
                parent=parent_relation
            )

        for obj in child_nodes_with_inverse:

            if obj['direction'] == 'REVENUE':
                direction = 1
            elif obj['direction'] == 'EXPENDITURE':
                direction = 2

            parent_relation = models[2].objects.get(
                code=obj['parent']
            )

            child_model = models[2].objects.create(
                template=head_model,
                code=obj['code'],
                name=obj['name'],
                direction=direction,
                parent=parent_relation
            )

            child_model.inverse.add(inverse_relation)

        return True


