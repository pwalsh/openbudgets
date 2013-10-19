requirejs.config({
    baseUrl : '/static/vendor',
    paths   : {
        jqscroll            : 'jqScroll/jqscroll',
        'jquery.mousewheel' : 'jquery-mousewheel',
        uijet_dir           : 'uijet',
        widgets             : 'uijet/widgets',
        composites          : 'uijet/composites',
        modules             : 'uijet/modules',
        comparisons         : '../tools/comparisons/comparisons',
        ui                  : '../tools/comparisons/ui',
        common_resources    : '../tools/comparisons/resources/commons',
        resources           : '../tools/comparisons/resources/tool',
        controllers         : '../tools/comparisons/controllers',
        tool_modules        : '../tools/comparisons/modules',
        tool_widgets        : '../tools/comparisons/widgets',
        tool_mixins         : '../tools/comparisons/mixins',
        dictionary          : '../tools/comparisons/dictionary',
        api                 : '../src/api',
        i18n                : '../src/i18n'
    },
    shim    : {
        d3                      : {
            exports : 'd3'
        },
        eventbox                : ['setImmediate'],
        'backbone-fetch-cache'  : 'modules/data/backbone'
    }
});
requirejs([
    'ui/main',
    '../js/base'
], function (comparisons) {

    comparisons.start();
});
