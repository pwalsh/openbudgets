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
            idAttribute : 'uuid'
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
            idAttribute : 'uuid'
        }),
        /*
         * BudgetTemplateNodes Collection
         */
        Nodes = uijet.Collection({
            model           : Node,
            parse           : function (response) {
                this._setAncestors(response);
                return response;
            },
            roots           : function () {
                return this.where({
                    parent  : null
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
            },
            _setAncestors   : function (response) {
                var len = response.length,
                    paths_lookup = {},
                    node, n, route, path;
                for ( n = len; node = response[n]; n-- ) {
                    node.ancestors = [];
                    paths_lookup[node.path] = node;
                }
                for ( n = len; node = response[n]; n-- ) {
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
            }
        });

    return {
        Munis   : Munis,
        Nodes   : Nodes
    };
});
