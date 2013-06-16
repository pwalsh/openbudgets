from datetime import datetime
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _, gettext as __
from openbudget.apps.budgets.models import Template, TemplateNode, TemplateNodeRelation
from openbudget.apps.entities.models import Division
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.transport.incoming.parsers import BaseParser, register, ParsingError
from openbudget.apps.transport.incoming.resolvers import PathResolver
from openbudget.apps.transport.incoming.errors import DataSyntaxError, ParentScopeError,\
    MetaParsingError, DataValidationError, NodeDirectionError, PathInterpolationError, ParentNodeNotFoundError


def _raise_parent_not_found(code, parent, scope):
    raise ParsingError(
        __('Could not locate parent of node: %s; with parent: %s; and scope: %s') %
        (code, parent, scope)
    )


class TemplateParser(BaseParser):

    container_model = Template
    item_model = TemplateNode
    ITEM_ATTRIBUTES = ['name', 'code', 'parent', 'path', 'templates', 'direction', 'description']\
        + translated_fields(TemplateNode)

    def __init__(self, container_object_dict, extends=None, fill_in_parents=None, interpolate=None):
        super(TemplateParser, self).__init__(container_object_dict)
        self.parent = extends
        self.skipped_rows = []

        #TODO: this assumes there's always a base template to inherit from, might need to support parents filling w/o parent template
        if extends:
            self.fill_in_parents = True if fill_in_parents is None else fill_in_parents
            self.interpolate = True if interpolate is None else interpolate
        else:
            self.fill_in_parents = False
            self.interpolate = False

        if self.interpolate:
            self.interpolated_lookup = {}

    def _save_item(self, obj, key, is_node=False):
        inverses = []
        item = None
        parent = None
        # check if we already saved this object and have it in cache
        if key in self.saved_cache:
            return self.saved_cache[key]

        # if it's a saved node it's already well connected
        if not is_node:
            # if inheriting another template then look up this node there
            if self.parent:
                path = obj['path']
                item = self._lookup_node(path=path, key=key)
                if item:
                    # in case we found the item, cache the saved node
                    return self._save_item(item, key, is_node=True)

                elif item is False:
                    # there's an ambiguity here that was caught
                    #TODO: handle case of ambiguity here
                    pass

                else:
                    # here we could note there's a delta between the templates
                    pass

            if 'inverse' in obj:
                inverses = self._save_inverses(obj, key)

            if 'parent' in obj:
                parent = self._save_parent(obj, key)
                if parent:
                    obj['parent'] = parent
                else:
                    # clean up parent
                    del obj['parent']

            # if inheriting another template AND got no parent AND didn't find
            # the item in the parent template then it has to be an error
            # unless we allow new parentless dangling nodes
            if self.dry and self.parent and not item and not parent:
                self.throw(
                    ParentNodeNotFoundError(
                        row=self.rows_objects_lookup.get(key, None),
                        columns=['code'],
                        values=[obj['code']]
                    )
                )

            self._set_direction(obj, parent)

            item = self._create_item(obj, key)

            if len(inverses) and not self.dry:
                for inverse in inverses:
                    item.inverse.add(inverse)

        else:
            if obj.parent:
                self._save_item(obj.parent, obj.parent.path, is_node=True)

            item = obj

        self._add_to_container(item, key)

        # cache the saved object
        self.saved_cache[key] = item

        return item

    def _save_inverses(self, obj, key):
        inverses = []
        inverse_codes = obj.get('inverse', None)
        scopes = obj.get('inversescope', None)

        if inverse_codes:
            inverse_codes = inverse_codes.split(self.ITEM_SEPARATOR)
        else:
            inverse_codes = []

        if len(inverse_codes):

            scopes_length = 0
            if scopes:
                scopes = scopes.split(self.ITEM_SEPARATOR)
                scopes_length = len(scopes)
                if not scopes_length:
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
                                row=self.rows_objects_lookup.get(key, None),
                                columns=('inverse', 'inversescope'),
                                values=(obj['inverse'], obj.get('inversescope', None))
                            )
                        )
                        # create a dummy node as the parent
                        inverse = self.item_model(code=obj['inverse'], name='dummy')
                    else:
                        raise ParsingError('Could not locate an inverse, \
                                        probably you have a syntax error: inverse = %s' % obj['inverse'])

                else:
                    if inverse_key in self.saved_cache:
                        inverse = self.saved_cache[inverse_key]
                    else:
                        inverse = self._save_item(inverse_obj, inverse_key)

                inverses.append(inverse)

                if self.dry:
                    if inverse.direction and inverse.direction == obj['direction']:
                        self.throw(
                            NodeDirectionError(
                                rows=(
                                    self.rows_objects_lookup.get(key, None),
                                    self.rows_objects_lookup.get(inverse_key, None)
                                )
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
                if not scope:
                    # clean parentscope
                    del obj['parentscope']
            else:
                scope = ''

            # generate a lookup key for the parent
            route = [unicode(obj['parent'])]
            if scope:
                route += scope.split(self.ROUTE_SEPARATOR)
            parent_path = self.ROUTE_SEPARATOR.join(route)

            # first look it up in the input from the source file
            parent_key, parent = self._lookup_object(key=parent_path)

            if not parent or not parent_key:

                if self.fill_in_parents:
                    # look up the node in the parent template
                    parent = self._lookup_node(path=parent_path, route=route, key=key)
                    if parent:
                        # save the node as if it was another object in the lookup
                        return self._save_item(parent, parent_path, is_node=True)

                    elif parent is False:
                        # there's an ambiguity here that was caught
                        if self.dry:
                            # create a dummy node as the parent
                            return self._create_dummy_parent(obj)
                        else:
                            _raise_parent_not_found(obj['code'], obj['parent'], scope)

                    elif self.interpolate and scope:
                        parent = self._interpolate(route=route, key=key)
                        if parent:
                            return parent
                        else:
                            return self._create_dummy_parent(obj)

                    else:
                        if self.dry:
                            self.throw(
                                ParentScopeError(
                                    row=self.rows_objects_lookup.get(key, None)
                                )
                            )
                            return self._create_dummy_parent(obj)
                        else:
                            _raise_parent_not_found(obj['code'], obj['parent'], scope)

                else:
                    if self.dry:
                        self.throw(
                            ParentNodeNotFoundError(
                                row=self.rows_objects_lookup.get(key, None)
                            )
                        )
                        # create a dummy node as the parent
                        return self._create_dummy_parent(obj)
                    else:
                        _raise_parent_not_found(obj['code'], obj['parent'], scope)

            else:
                if parent_key in self.saved_cache:
                    parent = self.saved_cache[parent_key]
                else:
                    parent = self._save_item(parent, parent_key)

                return parent

        else:
            if 'parentscope' in obj:
                # clean parentscope
                del obj['parentscope']

            return None

    def _create_dummy_parent(self, obj):
        code = obj['parent']
        attrs = {
            'code': code,
            'name': 'dummy',
        }

        direction = obj.get('direction', None)
        scope = obj.get('parentscope', None)
        path = code

        attrs['direction'] = direction or 'REVENUE'

        if scope:
            path = self.ROUTE_SEPARATOR.join((code, scope))

        attrs['path'] = path

        obj['parent'] = self.item_model(**attrs)
        return obj['parent']

    def _interpolate(self, route, key=None):
        route_copy = list(route)
        ancestors_routes = [route_copy]

        # first we'll try finding the other end
        while len(route):
            route.pop(0)
            ancestor = self._lookup_node(route=route, key=key)

            if ancestor:
                # connected!
                self._save_item(ancestor, self.ROUTE_SEPARATOR.join(route), is_node=True)
                break

            ancestors_routes.append(list(route))

        else:
            if self.dry:
                self.throw(
                    PathInterpolationError(
                        row=self.rows_objects_lookup[key]
                    )
                )
                return None
            else:
                raise ParsingError(_('Interpolation failed, no ancestor found for path: %s') %
                                   self.ROUTE_SEPARATOR.join(route_copy))

        # we managed to find an ancestor and saved it
        # now to connect the dots together,
        # i.e. create a node per route in `ancestors_routes`
        while len(ancestors_routes):
            ancestor_route = ancestors_routes.pop()
            ancestor = self._insert_item(ancestor_route, ancestor)

        return ancestor

    def _insert_item(self, route, parent, row_num=None):
        """
        Creates a new object representing an implicit parent node,
        adds it to the objects_lookup dictionary and saves it as an item.

        Takes a list `route` for determining the object's key and the item's
        code and parentscope.

        Also takes a node instance `parent` to set the item's parent and direction.

        Returns the product of `self._save_item()`.
        """
        key = self.ROUTE_SEPARATOR.join(route)
        code = route[0]
        parent_scope = ''

        if len(route) > 2:
            parent_scope = self.ROUTE_SEPARATOR.join(route[2:])

        obj = {
            'parent': parent,
            'code': code,
            'parentscope': parent_scope,
            'direction': parent.direction,
            'name': parent.name,
            'path': key
        }

        _key, _obj = self._lookup_object(key=key)
        if not _key:
            # self.objects_lookup[key] = obj
            if row_num is not None:
                self.rows_objects_lookup[key] = row_num

        else:
            raise ParsingError(_('You are trying to insert an item that already exists at: %s') % key)

        return self._save_item(obj, key)

    def _set_direction(self, obj, parent):
        if parent and ('direction' not in obj or not obj['direction']):
            obj['direction'] = parent.direction

    def _create_item(self, obj, key):
        # work with a clone so we always keep the source input
        obj = obj.copy()

        self._clean_object(obj, key)

        if not self.dry:
            item = self.item_model.objects.create(**obj)
        else:
            item = self.item_model(**obj)
            row_num = self.rows_objects_lookup.get(key, None)
            self._dry_clean(item, row_num=row_num)

        return item

    def _add_to_container(self, item, key):
        if not self.dry:
            try:
                TemplateNodeRelation.objects.create(
                    template=self.container_object,
                    node=item
                )
            except IntegrityError as e:
                #TODO: assuming here it's only the "columns node_id, template_id are not unique" error
                pass

    def _create_container(self, container_dict=None, exclude=None):

        data = (container_dict or self.container_object_dict).copy()

        if 'name' not in data:
            self._generate_container_name(container_dict=data)

        divisions = data.pop('divisions') if 'divisions' in data else []

        super(TemplateParser, self)._create_container(container_dict=data, exclude=exclude)

        for division in divisions:
            if not self.dry:
                self.container_object.divisions.add(division)
            else:
                try:
                    Division.objects.get(pk=division)
                except Division.DoesNotExist as e:
                    self.throw(
                        MetaParsingError(reason=_('DomainDivision with pk %s does not exist') % division)
                    )

    def _generate_lookup(self, data):
        self.resolver = PathResolver(parser=self, data=data, parent_template=self.parent)
        resolved = self.resolver.resolve()

        lookup_table = {}
        rows_objects_lookup = {}

        for key, (row_num, obj) in resolved.iteritems():
            keep_row = self._rows_filter(obj, row_num)
            if keep_row:
                lookup_table[key] = obj
                # +1 for heading row +1 for 0-based to 1-based
                rows_objects_lookup[key] = row_num + 2
            else:
                self._skipped_row(obj, row_num)

        self.objects_lookup = lookup_table
        self.rows_objects_lookup = rows_objects_lookup

    def _rows_filter(self, obj, row_num=None):
        return True

    def _skipped_row(self, obj, row_num):
        # +1 for heading row +1 for 0-based to 1-based
        self.skipped_rows.append((row_num + 2, obj))

    def _lookup_object(self, code=None, parent='', scope='', key=None):
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

        if key:
            if key in self.objects_lookup:
                return key, self.objects_lookup[key]

        return None, None

    def _lookup_node(self, route=None, path=None, key=None):
        if path is None:
            if route and len(route):
                path = self.ROUTE_SEPARATOR.join(route)

            else:
                raise ParsingError(
                    __('Did not get neither route nor path for looking up node, for row: %s') %
                    self.rows_objects_lookup.get(key, None)
                )

        try:
            # there can be one or none
            return self.parent.nodes.get(path=path)

        except TemplateNode.DoesNotExist as e:
            # none found
            try:
                if route is None and path:
                    route = path.split(self.ROUTE_SEPARATOR)
                _filter = {
                    'code': route[0]
                }
                if len(route) > 1:
                    _filter['parent__code'] = route[1]

                return self.parent.nodes.get(**_filter)

            except TemplateNode.DoesNotExist as e:
                return None
            except TemplateNode.MultipleObjectsReturned as e:
                if self.dry:
                    self.throw(
                        ParentScopeError(
                            row=self.rows_objects_lookup.get(key, None)
                        )
                    )
                    return False
                else:
                    raise e

        except TemplateNode.MultipleObjectsReturned as e:
            #TODO: this indicates that the data is corrupted, need to handle better
            if self.dry:
                # more then one probably means there's PARENT_SCOPE missing
                self.throw(
                    ParentScopeError(
                        row=self.rows_objects_lookup.get(key, None)
                    )
                )
                return False
            else:
                raise e

    def _generate_container_name(self, container_dict):
        name = _('Template of %(entity)s since %(year)s')
        year = str(datetime.strptime(container_dict['period_start'], '%Y-%m-%d').year)

        if 'entity' in container_dict and container_dict['entity']:
            entity = container_dict['entity']
            name = name % {'entity': entity.name, 'year': year}
            del container_dict['entity']

        elif 'divisions' in container_dict:
            name = _('Official Template since %(year)') % {'year': year}

        else:
            self.throw(
                DataValidationError(
                    reasons={'template': [__('Trying to create a template but no entity nor divisions found.')]}
                )
            )

        container_dict['name'] = name


register('template', TemplateParser)
