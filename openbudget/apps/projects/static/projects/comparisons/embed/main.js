requirejs.config({
    baseUrl : '/static/lib',
    paths   : {
        uijet_dir           : 'uijet',
        widgets             : 'uijet/widgets',
        composites          : 'uijet/composites',
        modules             : 'uijet/modules',
        comparisons            : '../projects/comparisons/comparisons',
        ui                  : '../projects/comparisons/embed/ui',
        resources           : '../projects/comparisons/resources',
        controllers         : '../projects/comparisons/controllers',
        project_modules     : '../projects/comparisons/modules',
        project_widgets     : '../projects/comparisons/widgets',
        project_mixins      : '../projects/comparisons/mixins',
        dictionary          : '../projects/comparisons/dictionary',
        api                 : '../src/api',
        i18n                : '../src/i18n'
    },
    shim    : {
        eventbox                : ['setImmediate'],
        'backbone-fetch-cache'  : 'modules/data/backbone'
    }
});

requirejs([
    'uijet_dir/uijet',
    'api',
    'resources',
    'modules/data/backbone',
    'modules/router/backbone',
    'modules/dom/jquery',
    'modules/pubsub/eventbox',
    'modules/promises/q',
    'modules/engine/mustache',
    'modules/xhr/jquery',
    'ui/embed'
], function (uijet, api, resources, Backbone, Router, $, ebox, Q, Mustache) {


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

    var routes_deferred = uijet.Promise(),
        routes_set_promise = routes_deferred.promise(),
        router = Router({
            routes  : {
                ':uuid' : function (uuid) {
                    var state = uijet.Resource('ProjectState');
                    if ( state.id !== uuid ) {
                        state.set({
                            uuid: uuid
                        })
                        .fetch({
                            success : function (model) {
                                var config = model.get('config'),
                                    series = config.chart,
                                    legend_data = uijet.Resource('TimeSeries').reset(series).extractLegend();
                                model.set({
                                    title       : config.title,
                                    description : config.description || '',
                                    normalize_by: config.normalize_by || null
                                });
                                legend_data.forEach(function (item, i) {
                                    item.state = series[i].state;
                                    item.title = series[i].title;
                                });
                                uijet.Resource('LegendItems').reset(legend_data).popColors();
                            },
                            error   : function (model, xhr, options) {
                                router.navigate('', { replace : true });
                            }
                        });
                    }
                }
            }
        });

    // set the API's routes
    api.getRoutes({
        success : function (response) {
            api._setRoutes(response);
            routes_deferred.resolve();
        }
    });

    /*
     * Register handlers to events in UI
     */
    uijet.subscribe('startup', function () {
        comparisons.routes_set_promise.then(function () {
            Backbone.history.start({
                pushState   : true,
                root        : '/tools/comparisons/'
            });
        });
    })
    /*
     * Starting uijet
     */
    .init({
        element             : 'article',
        templates_path      : '/static/projects/comparisons/templates/',
        templates_extension : 'ms'
    });

});
