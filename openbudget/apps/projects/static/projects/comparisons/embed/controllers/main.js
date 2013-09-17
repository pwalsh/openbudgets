define([
    'uijet_dir/uijet',
    'api',
    'resources',
    'modules/data/backbone',
    'modules/dom/jquery',
    'modules/pubsub/eventbox',
    'modules/promises/q',
    'modules/engine/mustache',
    'modules/xhr/jquery',
    'ui/main',
    'project_modules/uijet-i18n'
], function (uijet, api, resources, Backbone, $, ebox, Q, Mustache) {


    var state_config = window.STATE.config;
    // copy State related meta data to the config
    state_config.author = window.STATE.author;

    // make sure all jQuery requests (foreign and domestic) have a CSRF token 
    $(document).ajaxSend(function (event, xhr, settings) {
        if ( ! settings.headers )
            settings.headers = {};

        if ( ! ('X-CSRFToken' in settings.headers) )
            settings.headers['X-CSRFToken'] = api.getCSRFToken();
    });

    $(window).on('resize', function () {
        uijet.publish('app.resize');
    });

    // get version endpoint
    api.getVersion();

    // set the API's routes
    api.getRoutes({
        success : function (response) {
            api._setRoutes(response);
        }
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
        templates_path      : '/static/projects/comparisons/templates/',
        templates_extension : 'ms'
    });

});
