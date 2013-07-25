define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore',
    'api',
    'modules/promises/q',
    'backbone-fetch-cache'
], function (uijet, Backbone, _, api) {

    uijet.use({
        prop: function (property) {
            return function (obj) {
                return obj[property];
            };
        }
    }, uijet.utils);

    var reverseSorting = function (field) {
            return function (a, b) {
                var a_val = a.get(field),
                    b_val = b.get(field);
                return a_val < b_val ?
                    1 :
                    a_val > b_val ?
                        -1 :
                        0;
            };
        },
        nestingSort = function (a, b) {
            var a_attrs = a.attributes,
                b_attrs = b.attributes,
                a_parent = a_attrs.parent,
                b_parent = b_attrs.parent,
                collection, a_leaf, b_leaf;

            if ( a_parent === b_parent ) {
                a_leaf = a_attrs.leaf_node;
                b_leaf = b_attrs.leaf_node;
                if ( a_leaf && ! b_leaf )
                    return -1;
                else if ( b_leaf && ! a_leaf )
                    return 1;

                return a_attrs.code < b_attrs.code ? -1 : 1;
            }

            collection = a.collection;
            a_parent = a_parent ? collection.get(a_parent) : a;
            b_parent = b_parent ? collection.get(b_parent) : b;
            return nestingSort(a_parent, b_parent);
        },
        /*
         * User (Account) Model
         */
        User = uijet.Model({
            idAttribute : 'id',
            name: function () {
                var first = this.get('first_name'),
                    last = this.get('last_name');
                if ( first || last ) {
                    return first + ' ' + last;
                }
                else {
                    return gettext('Guest');
                }
            }
        }),
        /*
         * Muni (Entity) Model
         */
        Muni = uijet.Model({
            idAttribute : 'id'
        }),
        /*
         * Munis (Entities) Collection
         */
        Munis = uijet.Collection({
            model   : Muni,
            url     : function () {
                return api.getRoute('entities');
            },
            parse   : function (response) {
                //! Array.prototype.filter
                return response.results;
            }
        }),
        /*
         * TemplateNode Model
         */
        Node = uijet.Model({
            idAttribute : 'id'
        }),
        /*
         * TemplateNodes Collection
         */
        Nodes = uijet.Collection({
            model           : Node,
            url             : function () {
                return api.getRoute('templateNodes');
            },
            comparator      : function (a, b) {
                var a_attrs = a.attributes,
                    b_attrs = b.attributes,
                    diff = a_attrs.level - b_attrs.level;
                if ( ! diff ) {
                    diff = a_attrs.code < b_attrs.code;
                    return diff ?
                        -1 :
                        a_attrs.code > b_attrs.code ?
                            1 :
                            0;
                }
                return diff > 0 ? 1 : -1;
            },
            /**
             * Setting `ancestors` array of `id`s, `leaf_node` boolean flag and
             * `level` - a Number representing the level of the node in the tree.
             * 
             * @param {Object|Array} response
             * @returns {Object|Array} response
             */
            parse           : function (response) {
                var results = response.results,
                    last = results.length - 1,
                    paths_lookup = {},
                    parent_ids = {},
                    node, n, route, path, ancestor;
                /* 
                 * first loop
                 *
                 * init `ancestor` to `[]` 
                 * create `paths_lookup` to look up nodes by `path`
                 * create `parent_ids` to look up child nodes by `parent` (by id later)
                 * set `level` by splitting `path` and checking its `length`
                 * set `parent` to the parent's id
                 */
                for ( n = last; node = results[n]; n-- ) {
                    node.ancestors = [];
                    node.level = node.path.split('|').length - 1;
                    paths_lookup[node.path] = node;
                    if ( node.parent ) {
                        node.parent = node.parent.id || node.parent;
                        if ( ! parent_ids[node.parent] ) {
                            parent_ids[node.parent] = [];
                        }
                        parent_ids[node.parent].push(node.id);
                    }
                    node.direction = gettext(node.direction);
                }
                /*
                 * second loop
                 * 
                 * set `children` to the array in `parent_ids` using `id`
                 * set `leaf_node` to `true` if `id` is not in `parent_ids`
                 * fill `ancestors` array by ancestor `id`s ordered by `level` as index
                 */
                for ( n = last; node = results[n]; n-- ) {
                    if ( parent_ids[node.id] ) {
                        node.children = parent_ids[node.id];
                    }
                    else {
                        node.leaf_node = true;
                    }
                    route = node.path.split('|').slice(1);
                    while ( route.length ) {
                        path = route.join('|');
                        if ( path in paths_lookup ) {
                            ancestor = paths_lookup[path];
                            node.ancestors[ancestor.level] = ancestor.id;
                        }
                        route.shift();
                    }
                }
                paths_lookup = null;
                parent_ids = null;

                return results;
            },
            roots           : function () {
                return this.byParent(null);
            },
            byParent        : function (parent_id) {
                return this.where({
                    parent  : parent_id
                });
            },
            byAncestor      : function (ancestor_id) {
                if ( ancestor_id ) {
                    return this.filter(function (node) {
                        return ~ node.attributes.ancestors.indexOf(ancestor_id);
                    });
                }
                else {
                    return this.models;
                }
            },
            branch          : function (node_id) {
                var tip_node, branch;
                if ( node_id ) {
                    tip_node = this.get(node_id);
                    //! Array.prototype.map
                    branch = tip_node.get('ancestors')
                        .map( function (ancestor_id) {
                            return this.get(ancestor_id);
                        }, this );
                    branch.push(tip_node);
                }
                return branch || [];
            }
        }),
        State = uijet.Model({
            idAttribute : 'uuid',
            urlRoot     : function () {
                return api.getRoute('projectStates');
            },
            url         : function () {
                return this.urlRoot() + (this.id ? this.id + '/' : '');
            },
            parse       : function (response) {
                var user = new User(response.author);
                response.author_model = user;
                response.author = user.id;
                return response;
            }
        });

    return {
        User    : User,
        Muni    : Muni,
        Munis   : Munis,
        Node    : Node,
        Nodes   : Nodes,
        State   : State,
        utils   : {
            reverseSorting  : reverseSorting,
            nestingSort     : nestingSort
        },
        '_'     : _
    };
});
