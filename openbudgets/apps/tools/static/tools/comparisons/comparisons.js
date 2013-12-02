define([
    'uijet_dir/uijet',
    'resources',
    'controllers/AppState',
    'api',
    'modules/data/backbone',
    'modules/router/backbone',
    'modules/dom/jquery',
    'modules/pubsub/eventbox',
    'modules/promises/q',
    'modules/engine/mustache',
    'modules/xhr/jquery',
    'modules/animation/uijet-transit',
    'modules/search/uijet-search',
    'tool_modules/uijet-i18n'
], function (uijet, resources, state_controller, api, Backbone, Router, $, Ebox, Q, Mustache) {

    var default_state = {
            tool        : window.TOOL.id,
            author      : window.LOGGEDIN_USER.uuid,
            title       : '',
            description : '',
            author_model: new resources.User(window.LOGGEDIN_USER),
            id          : null,
            config      : null
        },
        comparisons;

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

    comparisons = {
        default_state   : default_state,
        router          : Router({
            routes  : {
                ':id'   : function (uuid) {
                    var state = uijet.Resource('ToolState');
                    if ( state.id !== id ) {
                        state.set({
                            id  : id
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
                                comparisons.router.navigate('', { replace : true });
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
//                    comparisons.setToken(auth_response.access_token);
//                }
//            });
            var routes_deferred = uijet.Promise();
            comparisons.routes_set_promise = routes_deferred.promise();

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
            uijet.Resource('Munis', resources.Munis)
                .Resource('LatestSheet', resources.Nodes)
                .Resource('Contexts', resources.Contexts)
                .Resource('LoggedinUser', resources.User, window.LOGGEDIN_USER)
                .Resource('TimeSeries', resources.TimeSeries);

            // add a sync event handler that caches IDs of Munis that their contexts where fetched
            uijet.Resource('Contexts')
                .on('sync', function (collection, response, options) {
                    collection.entities.push.apply(
                        collection.entities,
                        options.data.entities
                            .split(',')
                            .map(function (entity_id) {
                                return entity_id;
                            }));
                });

            this.LegendItemModel = uijet.Model({
                initialize  : function () {
                    this.id = this.id || resources._.uniqueId('li');
                }
            });

            uijet.Resource('LegendItems', uijet.Collection({
                model       : this.LegendItemModel,
                // for some reason this is need to prevent V8 from saying later that colors is undefined
                colors      : [],
                addColor    : function (color) {
                    this.colors.unshift(color);
                },
                popColors   : function () {
                    this.models.forEach(function (model) {
                        var index = this.colors.indexOf(model.get('color'));
                        if ( ~ index ) {
                            this.colors.splice(index, 1);
                        }
                    }, this);
                }
            }))

            .Resource('ToolState', resources.State, default_state);

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
            .subscribe('viz_new.clicked', comparisons.clearState)
            .subscribe('viz_save.clicked', comparisons.saveState)
            .subscribe('viz_duplicate.clicked', comparisons.duplicateState)
            .subscribe('viz_delete.clicked', comparisons.deleteState)
            .subscribe('login', function () {
                uijet.$('.login-link')[0].click();
            })


            /*
             * Starting uijet
             */
            .init({
                element             : '#comparisons',
                templates_path      : '/static/tools/comparisons/templates/',
                templates_extension : 'ms'
            });
        },
        setToken        : function (token) {
            this.auth_token = token;
            $.ajaxSetup({
                headers : {
                    Authorization   : 'Bearer ' + token
                }
            });
            uijet.publish('authenticated');
            return this;
        }
    };

    uijet.use(state_controller, comparisons, comparisons);

    return comparisons;
});
