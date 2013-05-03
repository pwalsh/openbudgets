requirejs.config({
    baseUrl : window.BASE_URL + 'lib',
    paths   : {
        uijet_dir   : 'uijet',
        composites  : 'uijet/composites',
        importer    : '../src/importer',
        ui          : '../src/importer/ui'
    },
    shim    : {
        eventbox                : ['setImmediate'],
        'composites/Datepicker' : ['importer/app']
    }
});
requirejs([
    'ui/main'
], function (Importer) {
    Importer.start();
});
