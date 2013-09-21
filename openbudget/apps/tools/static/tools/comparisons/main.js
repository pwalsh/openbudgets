requirejs.config({
    baseUrl : '/static/lib',
    paths   : {
        jqscroll            : 'jqScroll/jqscroll',
        'jquery.mousewheel' : 'jquery-mousewheel',
        uijet_dir           : 'uijet',
        widgets             : 'uijet/widgets',
        composites          : 'uijet/composites',
        modules             : 'uijet/modules',
        comparisons            : '../projects/comparisons/comparisons',
        ui                  : '../projects/comparisons/ui',
        common_resources    : '../projects/comparisons/resources/commons',
        resources           : '../projects/comparisons/resources/tool',
        controllers         : '../projects/comparisons/controllers',
        project_modules     : '../projects/comparisons/modules',
        project_widgets     : '../projects/comparisons/widgets',
        project_mixins      : '../projects/comparisons/mixins',
        dictionary          : '../projects/comparisons/dictionary',
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
