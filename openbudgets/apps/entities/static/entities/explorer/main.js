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
        explorer               : '../entities/explorer/explorer',
        ui                     : '../entities/explorer/ui',
        resources              : '../entities/explorer/resources',
        controllers            : '../entities/explorer/controllers',
        project_modules        : '../entities/explorer/modules',
        project_widgets        : '../entities/explorer/widgets',
        project_mixins         : '../entities/explorer/mixins',
        dictionary             : '../entities/explorer/dictionary',
        api                    : '../src/api',
        i18n                   : '../src/i18n'
    },
    shim    : {
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
], function (explorer) {

    explorer.start();
});
