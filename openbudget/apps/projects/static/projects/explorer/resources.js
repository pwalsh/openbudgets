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
                    return item.division.index === 3 && (item.budgets.length || item.actuals.length);
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
            model   : Node,
            past    : function (node_id, past) {
                var node = this.get(node_id),
                    backwards = node.get('backwards');
                past = past || [];
                _.each(backwards, function (id) {
                    past.push(id);
                    this.past(id, past);
                }, this);
                return past;
            },
            future  : function (node_id, future) {
                var node = this.get(node_id),
                    forwards = node.get('forwards');
                future = future || [];
                _.each(forwards, function (id) {
                    future.push(id);
                    this.future(id, future);
                }, this);
                return future;
            },
            timeline: function (node_id) {
                return[node_id].concat(this.future(node_id), this.past(node_id));
            }
        });

    return {
        Munis   : Munis,
        Nodes   : Nodes
    };
});
