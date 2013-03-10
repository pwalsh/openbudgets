requirejs.config({
    baseUrl : window.BASE_URL + 'js',
    paths   : {
        uijet_dir   : 'uijet/src',
        plugins     : '.',
        browser     : 'browser'
    }
});
requirejs(['browser/app'], function (Browser) {
    Browser.init();
});