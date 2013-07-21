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
    'project_modules/uijet-i18n',
    'project_modules/uijet-search'
], function (uijet, resources, api, Backbone, Router, $, Ebox, Q, Mustache) {

    var default_state = {
            project : 1,
            author  : 1,
            title   : gettext('Insert title')
        },
        explorer;

    // make sure all jQuery requests (foreign and domestic) have a CSRF token 
    $(document).ajaxSend(function (event, xhr, settings) {
        if ( ! settings.headers )
            settings.headers = {};

        if ( ! ('X-CSRFToken' in settings.headers) )
            settings.headers['X-CSRFToken'] = api.getCSRFToken();
    });
    // get version endpoint
    api.getVersion();

    explorer = {
        router      : Router({
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
                                model.set('title', config.title);
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
        start       : function (options) {
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

            .Resource('ProjectState', resources.State, default_state)

            // create a User model instance for representing the author of the state
            .Resource('Author', Backbone.Model.extend.call(resources.User, {
                name: function () {
                    var first = this.get('first_name'),
                        last = this.get('last_name');
                    if ( first || last ) {
                        return first + ' ' + last;
                    }
                    else {
                        return this.get('username');
                    }
                }
            }), {
                id  : uijet.Resource('ProjectState').get('author')
            });

            // once API routes are set init the router and sync the author
            explorer.routes_set_promise.then(function () {
                uijet.Resource('Author').fetch();
            });

            /*
             * Register handlers to events in UI
             */
            uijet.subscribe('startup', function () {
                explorer.routes_set_promise.then(function () {
                    Backbone.history.start({ root : 'static/projects/explorer/index.html' });
                });
            })
            .subscribe('viz_save.clicked', explorer.saveState)
            .subscribe('viz_new.clicked', explorer.clearState)

            /*
             * Starting uijet
             */
            .init({
                element             : '#explorer',
                templates_path      : '/static/projects/explorer/templates/',
                templates_extension : 'ms'
            });
        },
        setToken    : function (token) {
            this.auth_token = token;
            $.ajaxSetup({
                headers : {
                    Authorization   : 'Bearer ' + token
                }
            });
            uijet.publish('authenticated');
            return this;
        },
        clearState  : function () {
            uijet.Resource('TimeSeries').reset();
            uijet.Resource('LegendItems').reset();
            uijet.Resource('ProjectState').set(default_state);
            explorer.router.navigate('');
        },
        saveState   : function () {
            var chart_data = uijet.Resource('TimeSeries').toJSON(),
                legend = uijet.Resource('LegendItems'),
                selection_states = legend.pluck('state'),
                selection_titles = legend.pluck('title'),
                state_model = uijet.Resource('ProjectState');

            chart_data.forEach(function (series, i) {
                series.state = selection_states[i];
                series.title = selection_titles[i];
            });
            state_model.save({ config : {
                chart   : chart_data,
                title   : state_model.get('title')
            } }, {
                success : function () {
                    uijet.publish('state_saved');
                    explorer.router.navigate(state_model.get('uuid'));
                },
                error   : function () {
                    uijet.publish('state_save_failed');
                    console.error.apply(console, arguments);
                }
            });
        }
    };

    return explorer;
});
