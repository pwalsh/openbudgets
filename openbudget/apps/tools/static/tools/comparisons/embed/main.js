requirejs.config({
    baseUrl : '/static/lib',
    paths   : {
        uijet_dir           : 'uijet',
        widgets             : 'uijet/widgets',
        composites          : 'uijet/composites',
        modules             : 'uijet/modules',
        ui                  : '../projects/comparisons/embed/ui',
        resources           : '../projects/comparisons/embed/resources',
        app                 : '../projects/comparisons/embed/controllers/main',
        common_resources    : '../projects/comparisons/resources/commons',
        controllers         : '../projects/comparisons/controllers',
        project_modules     : '../projects/comparisons/modules',
        project_widgets     : '../projects/comparisons/widgets',
        project_mixins      : '../projects/comparisons/mixins',
        embed_widgets       : '../projects/comparisons/embed/widgets',
        dictionary          : '../projects/comparisons/dictionary',
        api                 : '../src/api',
        i18n                : '../src/i18n'
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
