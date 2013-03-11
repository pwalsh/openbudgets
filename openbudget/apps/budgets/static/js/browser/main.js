requirejs.config({
    baseUrl : window.BASE_URL + 'js',
    paths   : {
        uijet_dir   : 'uijet/src',
        plugins     : '.',
        browser     : 'browser',
        ui          : 'browser/ui',
        widgets     : 'browser/widgets',
        resources   : 'browser/resources'
    }
});
requirejs([
    'browser/app',
    'widgets/Table',
    'ui/main'
], function (Browser) {
    Browser.init();
});