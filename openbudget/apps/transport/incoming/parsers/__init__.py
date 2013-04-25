from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode,\
    BudgetTemplateNodeRelation, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.entities.models import Entity
from openbudget.apps.transport.incoming.errors import DataAmbiguityError


class BaseParser(object):

    def __init__(self, container_object_dict):
        self.valid = True
        self.errors = []
        self.container_object_dict = container_object_dict

    ROUTE_SEPARATOR = '|'
    ITEM_SEPARATOR = ';'
    saved_cache = {}
    objects_lookup = {}

    def validate(self, data):
        self._generate_lookup(data)
        return self.valid, self.errors

    def save(self):

        self._create_container()

        for key, obj in self.objects_lookup.iteritems():
            self._save_object(obj, key)

        return True

    def deferred(self):
        return {
            'container': self.container_object_dict,
            'items': self.objects_lookup
        }

    def throw(self, error):
        self.valid = False
        self.errors.append(error)
        return self

    def _generate_lookup(self, data):
        raise NotImplementedError

    def _save_object(self, obj, key):
        raise NotImplementedError

    def _create_container(self):
        raise NotImplementedError

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
        rows_objects_lookup = {}

        for row_num, obj in enumerate(objects):
            code = obj['code']

            if code in lookup_table:
                if code not in conflicting:
                    conflicting[code] = []
                conflicting[code].append((row_num, obj))
            else:
                lookup_table[code] = obj
                rows_objects_lookup[code] = row_num

        for code, obj_list in conflicting.iteritems():
            conflicting[code].append((rows_objects_lookup.pop(code), lookup_table.pop(code)))

        for code, obj_list in conflicting.iteritems():
            for row_num, obj in obj_list:
                # assuming there can't be two top level nodes with same code, naturally
                key = self.ROUTE_SEPARATOR.join((code, obj['parent']))
                # see if `parent` is also in conflict by looking for a `parentscope`
                if 'parentscope' in obj and obj['parentscope']:
                    key = key + self.ROUTE_SEPARATOR + obj['parentscope']

                if key in lookup_table:
                    self.throw(DataAmbiguityError(
                        rows=(row_num, rows_objects_lookup[key])
                    ))
                    # raise Exception('Found key: %s of object: %s colliding with: %s' % (key, obj, lookup_table[key]))

                lookup_table[key] = obj
                rows_objects_lookup[key] = row_num

        self.objects_lookup = lookup_table
        # self.rows_objects_lookup = rows_objects_lookup

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
