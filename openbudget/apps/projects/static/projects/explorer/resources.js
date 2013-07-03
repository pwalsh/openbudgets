define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore',
    'backbone-fetch-cache'
], function (uijet, Backbone, _) {

    uijet.use({
        prop: function (property) {
            return function (obj) {
                return obj[property];
            };
        }
    }, uijet.Utils);

    var
        reverseSorting = function (field) {
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
        });

    return {
        Munis   : Munis,
        Node    : Node,
        Nodes   : Nodes,
        utils   : {
            reverseSorting  : reverseSorting
        }
    };
});
