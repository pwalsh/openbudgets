requirejs.config({
    baseUrl : '/static/vendor',
    paths   : {
        jquery                 : 'jquery/jquery',
        jqscroll               : 'jqScroll/jqscroll',
        'jquery.mousewheel'    : 'jquery-mousewheel/jquery.mousewheel',
        backbone               : 'backbone/backbone',
        'backbone-fetch-cache' : 'backbone-fetch-cache/backbone.fetch-cache',
        d3                     : 'd3/d3',
        underscore             : 'underscore/underscore',
        mustache               : 'mustache/mustache',
        q                      : 'q/q',
        setImmediate           : 'setImmediate/setImmediate',
        eventbox               : 'eventbox/eventbox',
        uijet_dir              : 'uijet/src',
        widgets                : 'uijet/src/widgets',
        composites             : 'uijet/src/composites',
        modules                : 'uijet/src/modules',
        comparisons            : '../tools/comparisons/comparisons',
        ui                     : '../tools/comparisons/ui',
        common_resources       : '../tools/comparisons/resources/commons',
        resources              : '../tools/comparisons/resources/tool',
        controllers            : '../tools/comparisons/controllers',
        tool_modules           : '../tools/comparisons/modules',
        tool_widgets           : '../tools/comparisons/widgets',
        tool_mixins            : '../tools/comparisons/mixins',
        dictionary             : '../tools/comparisons/dictionary',
        api                    : '../src/api',
        i18n                   : '../src/i18n'
    },
    shim    : {
        d3                      : {
            exports : 'd3'
        },
        eventbox                : ['setImmediate'],
        'backbone-fetch-cache'  : 'modules/data/backbone',
        backbone                : {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        }
    }
});
requirejs([
    'ui/main',
    '../js/base'
], function (comparisons) {

    comparisons.start();
});
