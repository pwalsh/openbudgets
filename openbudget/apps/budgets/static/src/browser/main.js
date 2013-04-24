requirejs.config({
    baseUrl : window.BASE_URL + '/lib',
    paths   : {
        uijet_dir       : 'uijet',
        browser         : '../src/browser',
        ui              : '../src/browser/ui',
        widgets         : '../src/browser/widgets',
        adapters        : '../src/browser/adapters',
        resources       : '../src/browser/resources',
        storage         : '../src/storage'
    },
    shim    : {
        rickshaw: ['d3']
    }
});
requirejs([
    'ui/main'
], function (Browser) {
    Browser.start();
});
