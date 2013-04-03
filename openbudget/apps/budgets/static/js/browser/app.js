define([
    'settings',
    'uijet_dir/uijet',
    'uijet_dir/modules/dom/zepto',
    'uijet_dir/modules/pubsub/eventbox',
    'uijet_dir/modules/promises/q',
    'uijet_dir/modules/engine/mustache',
    'uijet_dir/modules/xhr/zepto',
    'resources',
    'underscore',
    'uijet_dir/modules/extensions/zepto-touch'
], function (SETTINGS, uijet, $, Ebox, Q, Mustache, Zepto_again, resources, _) {
    
    var Browser =  {
            BASE_API_URL: SETTINGS.BASE_API_URL,
            start       : function (options) {
                /*
                 * registering the collections' instances we'll be using in the Browser application
                 */
                uijet.Resource('Budgets', resources.Budgets);
                uijet.Resource('Actuals', resources.Actuals);
                uijet.Resource('Munis', resources.Munis);
                uijet.Resource('Items', resources.Items);

                /*
                 * subscribing to events in models
                 */
                uijet.subscribe({
                    budgets_updated : function (data) {
                        var items = [];
                        _.each(data.budgets, function (budget) {
                            items = items.concat(budget.items);
                        });
                        uijet.Resource('Items').reset(items);
                        uijet.publish('items_populated');
                    }
                });
                /*
                 * subscribing to events in views
                 */
                uijet.subscribe({
                    'munis_list.selected'   : this.pickMuni
                });

                /*
                 * Starting uijet
                 */
                uijet.init({
                    element             : '#budget_browser',
                    templates_path      : '/static/templates/',
                    templates_extension : 'ms'
                });
            },
            /**
             * @params muni {Object} - a Muni object as returned by the web API
             * @returns Browser
             */
            pickMuni    : function (muni) {
                Browser.current_muni = muni;

                // set collections' muni-dependant URL
                uijet.Resource('Budgets').setUrl(muni.url);
                uijet.Resource('Actuals').setUrl(muni.url);

                uijet.publish('MUNI_PICKED', muni.url);

                return Browser;
            }
        };

    return Browser;
});