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
            project     : 1,
            author      : 1,
            title       : gettext('Insert title'),
            description : ''
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
                .Resource('LatestSheet', resources.Nodes);
            
            this.LegendItemModel = uijet.Model({
                initialize  : function () {
                    this.id = resources._.uniqueId('li');
                }
            });

            uijet.Resource('LegendItems', uijet.Collection({
                model       : this.LegendItemModel,
                // for some reason this is need to prevent V8 from saying later that colors is undefined
                colors      : [],
                setColors   : function () {
                    this.models.forEach(function (model, index) {
                        model.set('color', this.colors[index]);
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
                        root        : '/projects/ext/comparisons/'
                    });
                });
            })
            .subscribe('viz_new.clicked', comparisons.clearState)
            .subscribe('viz_save.clicked', comparisons.saveState)
            .subscribe('viz_duplicate.clicked', comparisons.duplicateState)
            .subscribe('viz_delete.clicked', comparisons.deleteState)


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
            state_model.save({ config : {
                chart       : comparisons._getChartState(),
                title       : state_model.get('title'),
                description : state_model.get('description')
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
            comparisons.router.navigate('');
        },
        duplicateState  : function () {
            var state_clone = uijet.Resource('ProjectState').clone();
            state_clone.unset('uuid').unset('id').unset('url');
            //TODO: check if logged in user is same as state author and if yes set state author to user
            comparisons._saveState(state_clone);
        },
        saveState       : function () {
            comparisons._saveState(uijet.Resource('ProjectState'));
        },
        deleteState     : function () {
            //TODO: check (again) if logged in user is really the state author
            uijet.Resource('ProjectState').destroy({
                success : function () {
                    uijet.publish('state_deleted');
                    comparisons.router.navigate('');
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
