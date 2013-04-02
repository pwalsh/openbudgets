define([
    'uijet_dir/uijet',
    'uijet_dir/modules/data/backbone',
    'underscore'
], function (uijet, Backbone, _) {

    // base URL for the web API endpoint
    var host = window.location.host,
        BASE_API_URL = 'http://' + (host.split('.').length === 2 ? 'api.' + host : host.replace(/^([^\.]+)/, 'api')) + '/',

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
            parse   : function (response) {
                return response.node_set;
            },
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
        }),

        /*
         * SheetItem Model
         */
        Item = uijet.Model({
            idAttribute : 'uuid'
        }),
        /*
         * SheetItems Collection
         */
        Items = uijet.Collection({
            model   : Item,
            timeline: function (node) {
                
            }
        }),

        /*
         * Budget Model
         */
        Budget = uijet.Model({
            idAttribute : 'uuid'
        }),
        /*
         * Budgets Collection
         */
        Budgets = uijet.Collection({
            model   : Budget,
            parse   : function (response) {
                var budgets = response.budgets;
                uijet.publish('budgets_updated', {
                    collection  : this,
                    budgets     : budgets
                });
                return budgets;
            },
            setUrl  : function (entity_url) {
                this.url = entity_url;
            }
        }),

        /*
         * Actual Model
         */
        Actual = uijet.Model({
            idAttribute : 'uuid'
        }),
        /*
         * Actuals Collection
         */
        Actuals = uijet.Collection({
            model   : Actual,
            parse   : function (response) {
                return response.actuals;
            },
            setUrl  : function (entity_url) {
                this.url = entity_url;
            }
        }),

        /*
         * Muni (Entity) Model
         */
        Muni = uijet.Model({
            idAttribute : 'uuid'
        }),
        /*
         * Munis (Entiities) Collection
         */
        Munis = uijet.Collection({
            model   : Muni,
            url     : BASE_API_URL + 'domain-division/4/',
            parse   : function (response) {
                return response.entities;
            }
        });

    return {
        API_BASE: BASE_API_URL,
        Backbone: Backbone,
        Budgets : Budgets,
        Actuals : Actuals,
        Munis   : Munis,
        Nodes   : Nodes,
        Items   : Items
    };
});