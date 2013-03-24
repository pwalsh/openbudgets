define([
    'uijet_dir/uijet',
    'uijet_dir/modules/dom/zepto',
    'uijet_dir/modules/pubsub/eventbox',
    'uijet_dir/modules/promises/q',
    'uijet_dir/modules/engine/mustache',
    'uijet_dir/modules/xhr/zepto',
    'resources',
    'uijet_dir/modules/extensions/zepto-touch'
], function (uijet, $, Ebox, Q, Mustache, Zepto_again, resources) {
    
    var Browser =  {
            BASE_API_URL: resources.API_BASE,
            start       : function (options) {
                /*
                 * registering the collections' instances we'll be using in the Browser application
                 */
                uijet.Resource('Budgets', resources.Budgets);
                uijet.Resource('Actuals', resources.Actuals);
                uijet.Resource('Munis', resources.Munis);

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