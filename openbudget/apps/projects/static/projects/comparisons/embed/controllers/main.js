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
    'ui/main'
], function (uijet, api, resources, Backbone, $, ebox, Q, Mustache) {


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
    .Resource('TimeSeries', resources.TimeSeries, window.STATE.config.chart);

    return uijet.init.bind(uijet, {
        element             : 'article',
//        dont_cover          : true,
        templates_path      : '/static/projects/comparisons/templates/',
        templates_extension : 'ms'
    });

});
