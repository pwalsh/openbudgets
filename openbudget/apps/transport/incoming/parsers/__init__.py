from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode,\
    BudgetTemplateNodeRelation, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.entities.models import Entity, DomainDivision
from openbudget.apps.transport.incoming.errors import DataAmbiguityError, DataSyntaxError, ParentScopeError,\
    MetaParsingError, DataValidationError, NodeDirectionError, NodeNotFoundError


class BaseParser(object):

    def __init__(self, container_object_dict):
        self.valid = True
        self.dry = False
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

        self.dry = dry

        self._create_container()

        if dry:
            from copy import deepcopy
            # save an untempered copy
            lookup_table_copy = deepcopy(self.objects_lookup)

        for key, obj in self.objects_lookup.iteritems():
            self._save_object(obj, key)

        if dry:
            self.saved_cache.clear()
            # clear all changes by replacing the lookup with the old copy
            self.objects_lookup = lookup_table_copy

        self.dry = False

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

    def _create_container(self, container_dict=None):

        data = container_dict or self.container_object_dict

        if not self.dry:
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

    def _save_object(self, obj, key):
        inverses = []
        # check if we already saved this object and have it in cache
        if key in self.saved_cache:
            return self.saved_cache[key]

        if 'inverse' in obj:
            inverses = self._save_inverses(obj, key)

        if 'parent' in obj:
            self._save_parent(obj, key)

        item = self._create_item(obj, key)

        self._add_to_container(item, key)

        if len(inverses) and not self.dry:
            for inverse in inverses:
                item.inverse.add(inverse)

        # cache the saved object
        self.saved_cache[key] = item

        return item

    def _save_inverses(self, obj, key):
        inverses = []
        inverse_codes = obj['inverse'].split(self.ITEM_SEPARATOR)

        if len(inverse_codes) and inverse_codes[0]:
            scopes = []
            scopes_length = 0
            inverse_scope = ''

            if 'inversescope' in obj:
                inverse_scope = obj['inversescope']
                scopes = inverse_scope.split(self.ITEM_SEPARATOR)
                scopes_length = len(scopes)
                # clean up
                del obj['inversescope']

            for i, inv_code in enumerate(inverse_codes):
                if i < scopes_length:
                    inverse_key, inverse_obj = self._lookup_object(code=inv_code, scope=scopes[i])
                else:
                    inverse_key, inverse_obj = self._lookup_object(code=inv_code)

                if not inverse_key or not inverse_obj:
                    if self.dry:
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
                        inverse = self._save_object(inverse_obj, inverse_key)

                inverses.append(inverse)

                if self.dry:
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

        return inverses

    def _save_parent(self, obj, key):
        if obj['parent']:

            if 'parentscope' in obj:
                scope = obj['parentscope']
                # clean parentscope
                del obj['parentscope']
            else:
                scope = ''

            parent_key, parent = self._lookup_object(code=obj['parent'], scope=scope)

            if not parent or not parent_key:
                if self.dry:
                    self.throw(
                        ParentScopeError(
                            row=self.rows_objects_lookup[key]
                        )
                    )
                    # create a dummy node as the parent
                    obj['parent'] = self.item_model(code=obj['parent'], name='dummy', direction=obj['direction'])
                else:
                    raise Exception(
                        'Could not locate parent of node: %s; with parent: %s; and scope: %s' %
                        (obj['code'], obj['parent'], scope)
                    )

            else:
                if parent_key in self.saved_cache:
                    obj['parent'] = self.saved_cache[parent_key]
                else:
                    parent = self._save_object(parent, parent_key)
                    obj['parent'] = parent

        else:
            # clean parent
            del obj['parent']

            if 'parentscope' in obj:
                # clean parentscope
                del obj['parentscope']

    def _clean_object(self, obj, key):
        pass

    def _create_item(self, obj, key):
        self._clean_object(obj, key)
        if not self.dry:
            item = self.item_model.objects.create(**obj)
        else:
            item = self.item_model(**obj)
            self._dry_clean(item, row_num=self.rows_objects_lookup[key])
        return item

    def _add_to_container(self, item, key):
        if not self.dry:
            BudgetTemplateNodeRelation.objects.create(
                template=self.container_object,
                node=item
            )
        else:
            relation = BudgetTemplateNodeRelation()
            self._dry_clean(relation, row_num=self.rows_objects_lookup[key], exclude=['node', 'template'])

    def _create_container(self, container_dict=None):

        data = container_dict or self.container_object_dict

        dict_copy = data.copy()
        divisions = dict_copy.pop('divisions')

        super(BudgetTemplateParser, self)._create_container(container_dict=dict_copy)

        for division in divisions:
            if not self.dry:
                self.container_object.divisions.add(division)
            else:
                try:
                    DomainDivision.objects.get(pk=division)
                except DomainDivision.DoesNotExist as e:
                    self.throw(
                        MetaParsingError(reason=_('DomainDivision with pk %s does not exist') % division)
                    )

    def _generate_lookup(self, data):
        conflicting = {}
        lookup_table = {}
        rows_objects_lookup = {}

        for row_num, obj in enumerate(data):
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


class BudgetParser(BudgetTemplateParser):

    container_model = Budget
    item_model = BudgetItem

    def _save_object(self, obj, key):
        # check if we already saved this object and have it in cache
        if key in self.saved_cache:
            return self.saved_cache[key]

        self._add_to_container(obj, key)

        item = self._create_item(obj, key)

        # cache the saved object
        self.saved_cache[key] = item

    def _create_container(self, container_dict=None):

        data = container_dict or self.container_object_dict

        try:
            if not isinstance(data['entity'], Entity):
                entity = Entity.objects.get(
                    pk=data['entity']
                )
                data['entity'] = entity
        except Entity.DoesNotExist as e:
            if self.dry:
                self.throw(
                    MetaParsingError(
                        reason='Could not find Entity with key: %s' % data['entity']
                    )
                )
            else:
                raise e

        template = self._get_prev_template(data)
        #TODO: complete implementation of `_diff_template`
        # self._diff_template(template)

        data['template'] = template

        super(BudgetTemplateParser, self)._create_container(container_dict=data)

    def _clean_object(self, obj, key):
        #TODO: if customcode is important the handle it, or else remove altogether
        #TODO: first validate direction is compatible with node
        keys = ('customcode', 'direction', 'code', 'parent', 'parentscope', 'inverse', 'inversescope')
        for key in keys:
            if key in obj:
                del obj[key]

    def _create_item(self, obj, key):
        route = key.split(self.ROUTE_SEPARATOR)
        filter_key = 'code'

        _filter = {
            filter_key: route.pop(0)
        }

        while len(route):
            filter_key = 'parent__' + filter_key
            _filter[filter_key] = route.pop(0)

        try:
            #TODO: to optimize: replace with a cache of all nodes and look up in memory instead of hitting DB
            node = self.container_object.template.nodes.get(**_filter)
            obj['node'] = node
        except BudgetTemplateNode.DoesNotExist as e:
            if self.dry:
                # prepare data for the error
                columns = ['code', 'parent', 'parentscope']
                values = []
                for col in columns:
                    if col not in obj:
                        columns.remove(col)
                    else:
                        values.append(obj[col])
                self.throw(
                    NodeNotFoundError(
                        row=self.rows_objects_lookup[key],
                        columns=columns,
                        values=values
                    )
                )
            else:
                #TODO: handle this error properly, since at this stage there shouldn't be any missing nodes
                raise e

        self._clean_object(obj, key)
        if not self.dry:
            item = self.item_model.objects.create(**obj)
        else:
            item = self.item_model(**obj)
            self._dry_clean(item, self.rows_objects_lookup[key], exclude=['node', 'budget'])

        return item

    def _add_to_container(self, obj, key):
        if not self.dry:
            obj['budget'] = self.container_object

    def _get_prev_template(self, container_dict):

        entity = container_dict['entity']

        qs = self.container_model.objects.filter(
            entity=entity,
            period_end__lte=container_dict['period_start']
        ).order_by('-period_end')[:1]

        if qs.count():
            return qs[0].template
        else:
            # try getting the standard template for this entity's division
            qs = BudgetTemplate.objects.filter(divisions=entity.division).order_by('-period_start')[:1]
            if qs.count():
                return qs[0]
            else:
                #TODO: handle this case of no previous template found
                raise Exception

    def _diff_template(self, template):
        self.nodes = template.nodes
        for key, obj in self.objects_lookup.iteritems():
            route = key.split(self.ROUTE_SEPARATOR)
            self._lookup_node(obj=obj, route=route, nodes=self.nodes)

    def _lookup_node(self, obj, route, nodes, nodes_filter='code'):
        #TODO: probably need to replace the use of QuerySets and hitting the DB with plain in-memory lookups
        _filter = {
            nodes_filter: route.pop(0)
        }
        matches = nodes.filter(**_filter)
        count = matches.count()
        if count == 1:
            # bingo!
            return matches[0]
        elif count > 1:
            # continue filtering matches
            if len(route):
                return self._lookup_node(obj, route, matches, nodes_filter='parent__' + nodes_filter)
            else:
                # there was a code ambiguity in previous template but not in current one
                # probably some of the nodes with same code were removed
                #TODO: handle nodes removal
                pass
        else:
            #TODO: handle node with new code
            pass


class ActualParser(BudgetParser):

    container_model = Actual
    item_model = ActualItem


PARSERS_MAP = {
    'budgettemplate': BudgetTemplateParser,
    'budget': BudgetParser,
    'actual': ActualParser
}
