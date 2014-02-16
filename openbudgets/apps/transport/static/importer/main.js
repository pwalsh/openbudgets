requirejs.config({
    baseUrl : window.BASE_URL + 'vendor',
    paths   : {
        jqscroll            : 'jqScroll/jqscroll',
        'jquery.mousewheel' : 'jquery-mousewheel/jquery.mousewheel',
        setImmediate        : 'setImmediate/setImmediate',
        uijet_dir           : 'uijet/src',
        composites          : 'uijet/src/composites',
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
