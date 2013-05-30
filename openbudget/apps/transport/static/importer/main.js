requirejs.config({
    baseUrl : window.BASE_URL + 'lib',
    paths   : {
        jqscroll            : 'jqScroll/jqscroll',
        'jquery.mousewheel' : 'jquery-mousewheel',
        uijet_dir           : 'uijet',
        composites          : 'uijet/composites',
        importer            : '../importer',
        ui                  : '../importer/ui',
        controllers         : '../importer/controllers'
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
