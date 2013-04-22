requirejs.config({
    baseUrl : window.BASE_URL + '/lib',
    paths   : {
        uijet_dir       : 'uijet',
        importer        : '../src/importer',
        ui              : '../src/importer/ui'
    },
    shim    : {
        rickshaw: ['d3']
    }
});
requirejs([
    'ui/main'
], function (Importer) {
    Importer.start();
});
