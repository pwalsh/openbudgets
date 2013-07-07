requirejs.config({
    baseUrl : '/static/lib',
    paths   : {
        jqscroll            : 'jqScroll/jqscroll',
        'jquery.mousewheel' : 'jquery-mousewheel',
        uijet_dir           : 'uijet',
        composites          : 'uijet/composites',
        modules             : 'uijet/modules',
        explorer            : '../projects/explorer/explorer',
        ui                  : '../projects/explorer/ui',
        resources           : '../projects/explorer/resources',
        controllers         : '../projects/explorer/controllers',
        project_modules     : '../projects/explorer/modules',
        project_widgets     : '../projects/explorer/widgets',
        project_mixins      : '../projects/explorer/mixins',
        dictionary          : '../projects/explorer/i18n',
        api                 : '../src/api'
    },
    shim    : {
        eventbox                : ['setImmediate'],
        'backbone-fetch-cache'  : 'modules/data/backbone'
    }
});
requirejs([
    'ui/main'
], function (Explorer) {

    Explorer.start({
        AUTH_URL: window.AUTH_URL,
        auth    : {
            client_id       : '751be246011e8a6198d7',
            client_secret   : 'c62cb3b66fcbe46b82ecda2ed146b7bfe24fdea4',
            grant_type      : 'password',
            username        : 'pwalsh',
            password        : 'morelove!'
        }
    });
});
