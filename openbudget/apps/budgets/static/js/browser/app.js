define([
    'uijet_dir/uijet',
    'uijet_dir/modules/dom/zepto',
    'uijet_dir/modules/pubsub/eventbox',
    'uijet_dir/modules/promises/q',
    'uijet_dir/modules/engine/mustache',
    'uijet_dir/modules/data/backbone',
    'uijet_dir/modules/xhr/zepto'
], function (uijet, $, Ebox, Q, Mustache, Backbone) {
    
    var Browser =  {
            init: function (options) {
                uijet.init({
                    element             : '#budget_browser',
                    templates_path      : '/static/templates/',
                    templates_extension : 'ms'
                });
            }
        };

    return Browser;
});