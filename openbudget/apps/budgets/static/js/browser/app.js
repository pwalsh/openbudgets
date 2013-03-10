define([
    'uijet_dir/uijet',
    'uijet_dir/modules/dom/zepto',
    'uijet_dir/modules/pubsub/eventbox',
    'uijet_dir/modules/promises/q',
    'uijet_dir/modules/xhr/zepto'
], function (uijet, $, Ebox, Q, global) {
    
    var Browser =  {
            init: function (options) {
                uijet.init({
                    element : '#budget_browser'
                });
            }
        };

    return Browser;
});