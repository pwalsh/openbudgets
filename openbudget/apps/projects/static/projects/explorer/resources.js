define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore'
], function (uijet, Backbone, _) {

    var
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
            url     : API_URL + 'entity/',
            parse   : function (response) {
                //! Array.prototype.filter
                return response.results.filter(function (item) {
//                    return item.division.index === 3 && (item.budgets.length || item.actuals.length);
                    return item.division.index === 3;
                });
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
                        parent_ids[node.parent] = true;
                    }
                }
                for ( n = last; node = response[n]; n-- ) {
                    if ( ! parent_ids[node.id] ) {
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
                    }).map(function (model) {
                        return model.attributes;
                    });
                }
                else {
                    return this.toJSON();
                }
            },
            branch          : function (node_id) {
                //! Array.prototype.map
                return this.get(node_id).get('ancestors')
                    .map( function (ancestor_id) {
                        return this.get(ancestor_id).attributes;
                    }, this )
                    .sort( function (a, b) {
                        return a.level - b.level;
                    } );
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
        Nodes   : Nodes
    };
});
