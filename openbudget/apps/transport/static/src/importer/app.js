define([
    'uijet_dir/uijet',
    'uijet_dir/modules/dom/jquery',
    'uijet_dir/modules/pubsub/eventbox',
    'uijet_dir/modules/promises/q',
    'uijet_dir/modules/engine/mustache',
    'uijet_dir/modules/xhr/jquery'
], function (uijet, $, Ebox, Q, Mustache) {
    
    var Importer =  {
            BASE_API_URL: window.BASE_API_URL,
            start   : function (options) {
                /*
                 * subscribing to events in views
                 */
//                uijet.subscribe({});

                /*
                 * Starting uijet
                 */
                uijet.init({
                    element             : '#importer',
                    templates_path      : '/static/src/importer/templates/',
                    templates_extension : 'ms'
                });
            }
        };

    return Importer;
});
