from django.conf import settings
from openbudgets.apps.transport.incoming.parsers import ITEM_SEPARATOR
from openbudgets.apps.transport.incoming.errors import DataAmbiguityError, ParentScopeError,\
    InverseScopesError, InverseNodeNotFoundError


class PathResolver(object):

    #PATH_DELIMITER = settings.OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER
    PATH_DELIMITER = ','
    ITEM_SEPARATOR = ITEM_SEPARATOR

    def __init__(self, parser, data, parent_template=None):
        self.parser = parser
        self.raw_data = data

        self.parent_template = parent_template
        self.has_parent_template = True if parent_template else False

        self.resolved_lookup = {}
        self.resolved_rows_by_code = {}
        self.unresolved_rows_by_code = {}
        self.parent_nodes_by_code = {}
        self.root_nodes_lookup = {}
        self.parent_keys_lookup = []

    def resolve(self):
        first_run = []

        if self.parent_template:
            parent_nodes = self.parent_template.nodes.values('code', 'parent', 'path')
            for node in parent_nodes:
                code = node['code']
                if code not in self.parent_nodes_by_code:
                    self.parent_nodes_by_code[code] = []
                self.parent_nodes_by_code[code].append(node)
                if not node['parent']:
                    self.root_nodes_lookup[code] = node

        for row_num, obj in enumerate(self.raw_data):
            first_run.append((row_num, obj))

        next_run = self._resolve_paths(first_run)
        while len(next_run):
            next_run = self._resolve_paths(next_run, False)

        # one extra run for resolving inverses and marking nodes that `has_children`
        for key, row in self.resolved_lookup.iteritems():
            self._set_inverse_scope(row)
            obj = row[1]
            obj['has_children'] = obj['path'] in self.parent_keys_lookup

        if len(self.unresolved_rows_by_code):
            for code, rows in self.unresolved_rows_by_code.iteritems():
                for i, (row_num, obj) in enumerate(rows):
                    self._throw_parent_scope_error(obj['code'], obj.get('parent', ''), row_num)

        return self.resolved_lookup

    def throw(self, error):
        self.parser.throw(error)

    def _resolve_paths(self, data, first_run=True):
        #TODO: see where we lost the recognition of a DataAmbiguity along the way and throw it where needed
        next_run = []
        for row in data:
            row_num, obj = row
            code = obj.get('code', None)
            parent = obj.get('parent', None)
            if first_run:
                scope = obj.get('parentscope', None)
                if scope:


                    tmp = scope.split(self.PATH_DELIMITER)
                    scope = ','.join(tmp)  # tuple(tmp)


                if parent and scope:
                    # we have scope so we can resolve immediately
                    key = self.PATH_DELIMITER.join((code, parent, scope))
                    self._resolve_row(key, row)
                elif not parent:
                    # top level node - resolve
                    self._resolve_row(code, row)
                    self.root_nodes_lookup[code] = obj
                elif parent in self.root_nodes_lookup:
                    key = self.PATH_DELIMITER.join((code, self.root_nodes_lookup[parent]['code']))
                    self._resolve_row(key, row)
                else:
                    # defer for next run
                    self._defer_row(code, row, next_run)
            else:
                has_unresolved_parents = parent in self.unresolved_rows_by_code
                if parent in self.root_nodes_lookup:
                    key = self.PATH_DELIMITER.join((code, self.root_nodes_lookup[parent]['code']))
                    self._resolve_row(key, row)

                elif self.has_parent_template:
                    is_in_parent = parent in self.parent_nodes_by_code
                    is_in_resolved = parent in self.resolved_rows_by_code

                    if is_in_parent != is_in_resolved and not has_unresolved_parents:
                        if is_in_resolved and len(self.resolved_rows_by_code[parent]) == 1:
                            scope = self._get_scope_by_code(parent)
                            route = [code, parent]
                            if scope:
                                route += scope
                            key = self.PATH_DELIMITER.join(route)
                            self._resolve_row(key, row, self.PATH_DELIMITER.join(scope))
                        elif is_in_parent and len(self.parent_nodes_by_code[parent]) == 1:
                            scope = self._get_scope_by_code(parent, True)
                            route = [code, parent]
                            if scope:
                                route += scope
                            key = self.PATH_DELIMITER.join(route)
                            self._resolve_row(key, row, self.PATH_DELIMITER.join(scope))
                        else:
                            self._throw_parent_scope_error(code, parent, row_num)

                    elif is_in_parent:
                        self._throw_parent_scope_error(code, parent, row_num)

                    else:
                        # defer for next run
                        self._defer_row(code, row, next_run)

                else:
                    if parent in self.resolved_rows_by_code:
                        has_single_resolved_parent = len(self.resolved_rows_by_code[parent]) == 1
                        if has_single_resolved_parent and not has_unresolved_parents:
                            scope = self._get_scope_by_code(parent)
                            route = [code, parent]
                            if scope:
                                route += scope
                            key = self.PATH_DELIMITER.join(route)
                            self._resolve_row(key, row, self.PATH_DELIMITER.join(scope))
                        else:
                            self._throw_parent_scope_error(code, parent, row_num)
                    else:
                        # defer for next run
                        self._defer_row(code, row, next_run)

        return next_run if len(next_run) < len(data) else []

    def _throw_parent_scope_error(self, code, parent, row_num):
        self.throw(
            ParentScopeError(
                row=row_num + 2,
                columns=['code', 'parent'],
                values=[code, parent]
            )
        )

    def _resolve_row(self, key, row, scope=None):
        row_num, obj = row
        code = obj['code']
        if self.has_parent_template:
            self._remove_overridden_from_lookup(code, key)
        if scope:
            obj['parentscope'] = scope
        obj['path'] = key
        self.resolved_lookup[key] = row

        parent = obj.get('parent', None)
        if parent:
            scope = scope or obj.get('parentscope', None)
            parent_key = self.PATH_DELIMITER.join((parent, scope)) if scope else parent
            self.parent_keys_lookup.append(parent_key)

        if code not in self.resolved_rows_by_code:
            self.resolved_rows_by_code[code] = []
        self.resolved_rows_by_code[code].append(row)

        # remove row from unresolved lookup
        if code in self.unresolved_rows_by_code:
            list_copy = list(self.unresolved_rows_by_code[code])
            for i, (_row_num, _obj) in enumerate(list_copy):
                if _row_num == row_num:
                    self.unresolved_rows_by_code[code].pop(i)
                    # remove that code from the lookup if it's not containing any rows
                    if not len(self.unresolved_rows_by_code[code]):
                        del self.unresolved_rows_by_code[code]
                        break

    def _defer_row(self, code, row, next_run):
        next_run.append(row)
        if code not in self.unresolved_rows_by_code:
            self.unresolved_rows_by_code[code] = []
        self.unresolved_rows_by_code[code].append(row)

    def _lookup_path_in_parent(self, code, key, callback=None):
        if code in self.parent_nodes_by_code:
            for i, node in enumerate(self.parent_nodes_by_code[code]):
                if node['path'] == key:
                    if callback:
                        callback(i, node)
                    return True
        return False

    def _remove_overridden_from_lookup(self, code, key):
        def _remove_node(i, node):
            self.parent_nodes_by_code[code].pop(i)
        self._lookup_path_in_parent(code, key, _remove_node)

    def _get_scope_by_code(self, code, is_parent_node=False):
        if is_parent_node:
            parent_path = self.parent_nodes_by_code[code][0]['path']
        else:
            parent_path = self.resolved_rows_by_code[code][0][1]['path']
        return parent_path.split(self.PATH_DELIMITER)[1:]

    def _set_inverse_scope(self, row):
        row_num, obj = row
        inverse_codes = obj.get('inverse', None)
        inverse_scopes = obj.get('inversescope', None)
        if inverse_codes:
            inverses = inverse_codes.split(self.ITEM_SEPARATOR)

            if inverse_scopes:
                inverse_scopes = inverse_scopes.split(self.ITEM_SEPARATOR)

                if len(inverse_scopes) != len(inverses):
                    return self.throw(
                        InverseScopesError(
                            row=row_num,
                            columns=('inverse', 'inversescope'),
                            values=(inverse_codes, inverse_scopes)
                        )
                    )

                for i, inv_code in enumerate(inverses):
                    key = self.PATH_DELIMITER.join((inv_code, inverse_scopes[i]))
                    if key not in self.resolved_lookup and not self._lookup_path_in_parent(inv_code, key):
                        InverseNodeNotFoundError(
                            row=row_num,
                            columns=['inverse', 'inversescope'],
                            values=[obj.get('inverse'), obj.get('inversescope')]
                        )

            else:
                inverse_scopes = []
                for i, inv_code in enumerate(inverses):
                    if inv_code in self.root_nodes_lookup:
                        inverse_scopes.append('')
                    if inv_code in self.resolved_rows_by_code:
                        if len(self.resolved_rows_by_code[inv_code]) == 1:
                            scope = self.PATH_DELIMITER.join(self._get_scope_by_code(inv_code))
                            inverse_scopes.append(scope)
                        else:
                            self.throw(
                                InverseNodeNotFoundError(
                                    row=row_num,
                                    columns=['inverse', 'inversescope'],
                                    values=[obj.get('inverse'), obj.get('inversescope')]
                                )
                            )
                    elif inv_code in self.parent_nodes_by_code and len(self.parent_nodes_by_code[inv_code]) == 1:
                        scope = self.PATH_DELIMITER.join(self._get_scope_by_code(inv_code, True))
                        inverse_scopes.append(scope)
                    else:
                        self.throw(
                            InverseNodeNotFoundError(
                                row=row_num,
                                columns=['inverse', 'inversescope'],
                                values=[obj.get('inverse'), obj.get('inversescope')]
                            )
                        )
                if len(inverse_scopes):
                    obj['inversescope'] = self.ITEM_SEPARATOR.join(inverse_scopes)
