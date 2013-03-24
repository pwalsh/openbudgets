define([
    'uijet_dir/uijet',
    'uijet_dir/modules/data/backbone'
], function (uijet, Backbone) {

    // base URL for the web API endpoint
    var BASE_API_URL = 'http://api.obudget.dev:8000/',

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
            model       : Budget,
            url         : BASE_API_URL + 'budgets/',
            parse       : function (response) {
                return response.budgets;
            },
            setUrl      : function (entity_url) {
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
            model       : Actual,
            url         : BASE_API_URL + 'actuals/',
            parse       : function (response) {
                return response.actuals;
            },
            setUrl      : function (entity_url) {
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
            model       : Muni,
            url         : BASE_API_URL + 'domain-division/4/',
            parse       : function (response) {
                return response.entities;
            }
        });

    return {
        API_BASE: BASE_API_URL,
        Backbone: Backbone,
        Budget  : Budget,
        Budgets : Budgets,
        Actual  : Actual,
        Actuals : Actuals,
        Muni    : Muni,
        Munis   : Munis
    };
});