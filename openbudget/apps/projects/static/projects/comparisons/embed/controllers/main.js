define([
    'uijet_dir/uijet',
    'resources',
    'modules/data/backbone',
    'modules/dom/jquery',
    'modules/pubsub/eventbox',
    'modules/promises/q',
    'modules/engine/mustache',
    'modules/xhr/jquery',
    'ui/main',
    'project_modules/uijet-i18n'
], function (uijet, resources, Backbone, $, ebox, Q, Mustache) {


    var state_config = window.STATE.config;
    // copy State related meta data to the config
    state_config.author = window.STATE.author;

    $(window).on('resize', function () {
        uijet.publish('app.resize');
    });

    /*
     * Register resources
     */
    uijet
    .Resource('Munis', resources.Munis)
    .Resource('TimeSeries', resources.TimeSeries, state_config.chart)
    .Resource('ProjectState', resources.State, state_config, { parse : true });

    return uijet.init.bind(uijet, {
        element             : 'article',
//        dont_cover          : true,
        templates_path      : '/static/projects/comparisons/embed/templates/',
        templates_extension : 'ms'
    });

});
