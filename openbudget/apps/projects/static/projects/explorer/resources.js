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
        });

    return {
        Munis   : Munis
    };
});
