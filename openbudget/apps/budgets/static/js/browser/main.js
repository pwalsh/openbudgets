requirejs.config({
    baseUrl : window.BASE_URL + 'js/lib',
    paths   : {
        uijet_dir       : 'uijet',
        plugins         : '.',
        'zepto-touch'   : 'touch',
        browser         : '../browser',
        ui              : '../browser/ui',
        widgets         : '../browser/widgets',
        adapters        : '../browser/adapters',
        resources       : '../browser/resources'
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