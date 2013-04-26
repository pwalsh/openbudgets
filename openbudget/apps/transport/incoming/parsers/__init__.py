from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode,\
    BudgetTemplateNodeRelation, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.entities.models import Entity, DomainDivision
from openbudget.apps.transport.incoming.errors import DataAmbiguityError, DataSyntaxError, ParentScopeError,\
    MetaParsingError, DataValidationError, NodeDirectionError


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
        self.save(dry=True)
        return self.valid, self.errors

    def save(self, dry=False):

        self._create_container(dry=dry)

        for key, obj in self.objects_lookup.iteritems():
            self._save_object(obj, key, dry=dry)

        if dry:
            self.saved_cache.clear()

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

    def _save_object(self, obj, key, dry=False):
        raise NotImplementedError

    def _create_container(self, container_dict=None, dry=False):

        data = container_dict or self.container_object_dict

        if not dry:
            container = self.container_model.objects.create(**data)
        else:
            container = self.container_model(**data)
            self._dry_clean(container)

        self.container_object = container

    def _dry_clean(self, instance, row_num=None, exclude=None):
        try:
            instance.full_clean(exclude=exclude)
        except ValidationError as e:
            self.throw(
                DataValidationError(reasons=e.message_dict, row=row_num)
            )

class BudgetTemplateParser(BaseParser):

    container_model = BudgetTemplate
    item_model = BudgetTemplateNode

    def _save_object(self, obj, key, dry=False):
        inverses = []
        # check if we already saved this object and have it in cache
        if key in self.saved_cache:
            return self.saved_cache[key]

        if 'inverse' in obj:
            inverse_codes = obj['inverse'].split(self.ITEM_SEPARATOR)

            if len(inverse_codes) and inverse_codes[0]:
                scopes = []
                inverse_scope = ''

                if 'inversescope' in obj:
                    inverse_scope = obj['inversescope']
                    scopes = inverse_scope.split(self.ITEM_SEPARATOR)
                    # clean up
                    del obj['inversescope']

                for i, inv_code in enumerate(inverse_codes):
                    if i in scopes:
                        inverse_key, inverse_obj = self._lookup_object(code=inv_code, scope=scopes[i])
                    else:
                        inverse_key, inverse_obj = self._lookup_object(code=inv_code)

                    if not inverse_key or not inverse_obj:
                        if dry:
                            self.throw(
                                DataSyntaxError(
                                    row=self.rows_objects_lookup[key],
                                    columns=('inverse', 'inversescope'),
                                    values=(obj['inverse'], inverse_scope)
                                )
                            )
                            # create a dummy node as the parent
                            inverse = self.item_model(code=obj['inverse'], name='dummy')
                        else:
                            raise Exception('Could not locate an inverse, \
                                            probably you have a syntax error: inverse = %s' % obj['inverse'])

                    else:
                        if inverse_key in self.saved_cache:
                            inverse = self.saved_cache[inverse_key]
                        else:
                            inverse = self._save_object(inverse_obj, inverse_key, dry=dry)

                    inverses.append(inverse)

                    if dry:
                        if inverse.direction and inverse.direction == obj['direction']:
                            self.throw(
                                NodeDirectionError(
                                    rows=(self.rows_objects_lookup[key], self.rows_objects_lookup[inverse_key])
                                )
                            )

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

            if not parent or not parent_key:
                if dry:
                    self.throw(
                        ParentScopeError(
                            row=self.rows_objects_lookup[key]
                        )
                    )
                    # create a dummy node as the parent
                    obj['parent'] = self.item_model(code=obj['parent'], name='dummy', direction=obj['direction'])
                else:
                    raise

            else:
                if parent_key in self.saved_cache:
                    obj['parent'] = self.saved_cache[parent_key]
                else:
                    parent = self._save_object(parent, parent_key, dry=dry)
                    obj['parent'] = parent

        elif 'parent' in obj:
            # clean parent
            del obj['parent']

            if 'parentscope' in obj:
                # clean parentscope
                del obj['parentscope']

        if not dry:
            item = self.item_model.objects.create(**obj)

            BudgetTemplateNodeRelation.objects.create(
                template=self.container_object,
                node=item
            )
        else:
            item = self.item_model(**obj)
            self._dry_clean(item, row_num=self.rows_objects_lookup[key])

            relation = BudgetTemplateNodeRelation()
            self._dry_clean(relation, row_num=self.rows_objects_lookup[key], exclude=('node', 'template'))

        if len(inverses) and not dry:
            for inverse in inverses:
                item.inverse.add(inverse)

        # cache the saved object
        self.saved_cache[key] = item

        return item

    def _create_container(self, container_dict=None, dry=False):

        data = container_dict or self.container_object_dict

        dict_copy = data.copy()
        divisions = dict_copy.pop('divisions')

        super(BudgetTemplateParser, self)._create_container(container_dict=dict_copy, dry=dry)

        for division in divisions:
            if not dry:
                self.container.divisions.add(division)
            else:
                try:
                    DomainDivision.objects.get(pk=division)
                except DomainDivision.DoesNotExist as e:
                    self.throw(
                        MetaParsingError(reason=_('DomainDivision with pk %s does not exist') % division)
                    )

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
                    self.throw(
                        DataAmbiguityError(
                            rows=(row_num, rows_objects_lookup[key])
                        )
                    )
                    # raise Exception('Found key: %s of object: %s colliding with: %s' % (key, obj, lookup_table[key]))

                lookup_table[key] = obj
                rows_objects_lookup[key] = row_num

        self.objects_lookup = lookup_table
        self.rows_objects_lookup = rows_objects_lookup

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

    def _create_container(self, container_dict=None, dry=False):

        data = container_dict or self.container_object_dict

        if not dry:
            entity = Entity.objects.get(
                pk=data['entity']
            )
        else:
            entity = Entity(pk=data['entity'])
            self._dry_clean(entity)

        data['entity'] = entity

        super(BudgetParser, self)._create_container(container_dict=data, dry=dry)


class ActualParser(BudgetParser):

    container_model = Actual
    item_model = ActualItem


PARSERS_MAP = {
    'budgettemplate': BudgetTemplateParser,
    'budget': BudgetParser,
    'actual': ActualParser
}
