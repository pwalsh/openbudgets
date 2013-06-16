define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore'
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
            url     : API_URL + 'entities/?division__budgeting=True',
            parse   : function (response) {
                //! Array.prototype.filter
                return response.results;
            }
        }),
        /*
         * BudgetTemplateNode Model
         */
        Node = uijet.Model({
            idAttribute : 'id'
        }),
        /*
         * BudgetTemplateNodes Collection
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
                var last = response.length - 1,
                    paths_lookup = {},
                    parent_ids = {},
                    node, n, route, path;
                for ( n = last; node = response[n]; n-- ) {
                    node.ancestors = [];
                    paths_lookup[node.path] = node;
                    if ( node.parent ) {
                        if ( ! parent_ids[node.parent] ) {
                            parent_ids[node.parent] = [];
                        }
                        parent_ids[node.parent].push(node.id);
                    }
                }
                for ( n = last; node = response[n]; n-- ) {
                    if ( parent_ids[node.id] ) {
                        node.children = parent_ids[node.id];
                    }
                    else {
                        node.leaf_node = true;
                    }
                    route = node.path.split('|').slice(1);
                    node.level = route.length;
                    while ( route.length ) {
                        path = route.join('|');
                        if ( path in paths_lookup ) {
                            node.ancestors.push(paths_lookup[path].id);
                        }
                        route.shift();
                    }
                }
                paths_lookup = null;
                parent_ids = null;

                return response;
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
                        }, this )
                        .sort( function (a, b) {
                            return a.attributes.level - b.attributes.level;
                        } );
                    branch.push(tip_node);
                }
                return branch || [];
            },
            past            : function (node_id, past) {
                var node = this.get(node_id),
                    backwards = node.get('backwards');
                past = past || [];
                _.each(backwards, function (id) {
                    past.push(id);
                    this.past(id, past);
                }, this);
                return past;
            },
            future          : function (node_id, future) {
                var node = this.get(node_id),
                    forwards = node.get('forwards');
                future = future || [];
                _.each(forwards, function (id) {
                    future.push(id);
                    this.future(id, future);
                }, this);
                return future;
            },
            timeline        : function (node_id) {
                return[node_id].concat(this.future(node_id), this.past(node_id));
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
