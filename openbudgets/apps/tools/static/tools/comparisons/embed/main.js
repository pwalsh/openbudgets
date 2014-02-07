requirejs.config({
    baseUrl : '/static/vendor',
    paths   : {
        uijet_dir       : 'uijet',
        widgets         : 'uijet/src/widgets',
        composites      : 'uijet/src/composites',
        modules         : 'uijet/src/modules',
        setImmediate    : 'setImmediate/setImmediate',
        ui              : '../tools/comparisons/embed/ui',
        resources       : '../tools/comparisons/embed/resources',
        app             : '../tools/comparisons/embed/controllers/main',
        common_resources: '../tools/comparisons/resources/commons',
        controllers     : '../tools/comparisons/controllers',
        tool_modules    : '../tools/comparisons/modules',
        tool_widgets    : '../tools/comparisons/widgets',
        tool_mixins     : '../tools/comparisons/mixins',
        embed_widgets   : '../tools/comparisons/embed/widgets',
        dictionary      : '../tools/comparisons/dictionary',
        api             : '../src/api',
        i18n            : '../src/i18n'
    },
    shim    : {
        eventbox                : ['setImmediate'],
        'backbone-fetch-cache'  : 'modules/data/backbone',
        'ui/main'               : 'resources'
    }
});

requirejs([
    'ui/main'
]);
