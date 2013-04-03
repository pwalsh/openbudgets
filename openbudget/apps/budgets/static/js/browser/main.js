requirejs.config({
    baseUrl : window.BASE_URL + 'js/lib',
    paths   : {
        settings        : '../settings',
        uijet_dir       : 'uijet',
        'zepto-touch'   : 'touch',
        browser         : '../browser',
        ui              : '../browser/ui',
        widgets         : '../browser/widgets',
        adapters        : '../browser/adapters',
        resources       : '../browser/resources'
    },
    shim    : {
        rickshaw: ['d3'],
        touch   : ['zepto']
    }
});
requirejs([
    'ui/main'
], function (Browser) {
    Browser.start();
});