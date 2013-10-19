requirejs.config({
    baseUrl : window.BASE_URL + 'vendor',
    paths   : {
        jqscroll            : 'jqScroll/jqscroll',
        'jquery.mousewheel' : 'jquery-mousewheel',
        uijet_dir           : 'uijet',
        composites          : 'uijet/composites',
        importer            : '../importer',
        ui                  : '../importer/ui',
        controllers         : '../importer/controllers',
        i18n                : '../importer/i18n'
    },
    shim    : {
        eventbox: ['setImmediate']
    }
});
requirejs([
    'ui/main'
], function (Importer) {
    Importer.start();
});
