requirejs.config({
    baseUrl : '/static/lib',
    paths   : {
        jqscroll            : 'jqScroll/jqscroll',
        'jquery.mousewheel' : 'jquery-mousewheel',
        uijet_dir           : 'uijet',
        widgets             : 'uijet/widgets',
        composites          : 'uijet/composites',
        modules             : 'uijet/modules',
        explorer            : '../entities/explorer/explorer',
        ui                  : '../entities/explorer/ui',
        resources           : '../entities/explorer/resources',
        controllers         : '../entities/explorer/controllers',
        project_modules     : '../entities/explorer/modules',
        project_widgets     : '../entities/explorer/widgets',
        project_mixins      : '../entities/explorer/mixins',
        dictionary          : '../entities/explorer/dictionary',
        api                 : '../src/api',
        i18n                : '../src/i18n'
    },
    shim    : {
        eventbox                : ['setImmediate'],
        'backbone-fetch-cache'  : 'modules/data/backbone'
    }
});
requirejs([
    'ui/main'
], function (explorer) {

    explorer.start();
});
