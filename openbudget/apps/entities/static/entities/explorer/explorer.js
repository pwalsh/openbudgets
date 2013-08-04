define([
    'uijet_dir/uijet',
    'resources',
    'api',
    'modules/data/backbone',
    'modules/router/backbone',
    'modules/dom/jquery',
    'modules/pubsub/eventbox',
    'modules/promises/q',
    'modules/engine/mustache',
    'modules/xhr/jquery',
    'modules/animation/uijet-transit',
    'modules/search/uijet-search'
//    'project_modules/uijet-i18n',
], function (uijet, resources, api, Backbone, Router, $, Ebox, Q, Mustache) {

    var explorer;

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

    explorer = {
        router          : Router({
            routes  : {
                ':uuid' : function (uuid) {
                    var state = uijet.Resource('ProjectState');
                    if ( state.id !== uuid ) {
                        state.set({
                            uuid: uuid
                        })
                        .fetch({
                            success : function (model) {
                                var config = JSON.parse(model.get('config')),
                                    series = config.chart,
                                    legend_data = uijet.Resource('TimeSeries').reset(series).extractLegend();
                                model.set({
                                    title       : config.title || gettext('Insert title'),
                                    description : config.description || ''
                                });
                                legend_data.forEach(function (item, i) {
                                    item.state = series[i].state;
                                    item.title = series[i].title;
                                });
                                uijet.Resource('LegendItems').reset(legend_data);
                            }
                        });
                    }
                }
            }
        }),
        start           : function (options) {
            /*
             * Get an OAuth2 token
             */
//            api.auth({
//                data    : options.auth,
//                success : function (auth_response) {
                    // set the API's routes
//                    api.getRoutes({
//                        success : function (response) {
//                            api._setRoutes(response);
//                            uijet.publish('api_routes_set');
//                        }
//                    });
//                    explorer.setToken(auth_response.access_token);
//                }
//            });
            var routes_deferred = uijet.Promise();
            explorer.routes_set_promise = routes_deferred.promise();

            // set the API's routes
            api.getRoutes({
                success : function (response) {
                    api._setRoutes(response);
                    routes_deferred.resolve();
                }
            });
            /*
             * Register resources
             */
            uijet.Resource('LatestSheet', resources.Nodes);

            /*
             * Register handlers to events in UI
             */
            uijet.subscribe('startup', function () {
                explorer.routes_set_promise.then(function () {
                    Backbone.history.start({
                        pushState   : true,
                        root        : '/entities/explorer/'
                    });
                });
            })

            /*
             * Starting uijet
             */
            .init({
                element             : '#explorer',
                templates_path      : '/static/entities/explorer/templates/',
                templates_extension : 'ms'
            });
        }
    };

    return explorer;
});
