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
    'modules/search/uijet-search',
    'project_modules/uijet-i18n'
], function (uijet, resources, api, Backbone, Router, $, Ebox, Q, Mustache) {

    var default_state = {
            project     : window.PROJECT.uuid,
            author      : window.LOGGEDIN_USER.uuid,
            title       : gettext('Insert title'),
            description : '',
            author_model: new resources.User(window.LOGGEDIN_USER),
            uuid        : null,
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
                .Resource('LoggedinUser', resources.User, window.LOGGEDIN_USER);

            // add a sync event handler that caches IDs of Munis that their contexts where fetched
            uijet.Resource('Contexts').on('sync', function (collection, response, options) {
                collection.entities.push.apply(
                    collection.entities,
                    options.data.entities
                        .split(',')
                        .map(function (entity_id) {
                            return +entity_id;
                        }));
            });

            this.LegendItemModel = uijet.Model({
                initialize  : function () {
                    this.id = resources._.uniqueId('li');
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

            .Resource('ProjectState', resources.State, default_state);

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
                templates_path      : '/static/projects/comparisons/templates/',
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
        },
        _getChartState  : function () {
            var chart_data = uijet.Resource('TimeSeries').toJSON(),
                legend = uijet.Resource('LegendItems'),
                selection_states = legend.pluck('state'),
                selection_titles = legend.pluck('title');

            chart_data.forEach(function (series, i) {
                series.state = selection_states[i];
                series.title = selection_titles[i];
            });
            return chart_data;
        },
        _saveState      : function (state_model) {
            var nodes_list_state = uijet.Resource('NodesListState');
            return state_model.save({ config : {
                chart       : comparisons._getChartState(),
                title       : state_model.get('title'),
                description : state_model.get('description'),
                normalize_by: nodes_list_state.get('normalize_by')
            } }, {
                success : function () {
                    uijet.publish('state_saved');
                    comparisons.router.navigate(state_model.get('uuid'));
                },
                error   : function () {
                    uijet.publish('state_save_failed');
                    console.error.apply(console, arguments);
                }
            });
        },
        clearState      : function () {
            uijet.Resource('TimeSeries').reset();
            uijet.Resource('LegendItems').reset();
            uijet.Resource('ProjectState').set(default_state);
            uijet.publish('state_cleared');
            comparisons.router.navigate('');
        },
        duplicateState  : function () {
            var state_clone = uijet.Resource('ProjectState').clone(),
                user = uijet.Resource('LoggedinUser');
            state_clone
                .unset('uuid')
                .unset('id')
                .unset('url')
                .set({
                    author      : user.get('uuid'),
                    author_model: user
                });
            return comparisons._saveState(state_clone);
        },
        saveState       : function () {
            var state = uijet.Resource('ProjectState'),
                user_uuid = uijet.Resource('LoggedinUser').get('uuid');
            if ( user_uuid ) {
                if ( state.get('author') === user_uuid ) {
                    return comparisons._saveState(state);
                }
                else {
                    return comparisons.duplicateState();
                }
            }
            else {
                return uijet.publish('login')
                    .Promise()
                        .reject('User not logged in')
                        .promise();
            }
        },
        deleteState     : function () {
            //TODO: check (again) if logged in user is really the state author
            return uijet.Resource('ProjectState').destroy({
                success : function () {
                    comparisons.clearState();
                },
                error   : function () {
                    uijet.publish('state_delete_failed');
                    console.error.apply(console, arguments);
                }
            });
        }
    };

    return comparisons;
});
