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

    var explorer;

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
                                var series = JSON.parse(model.get('config')),
                                    legend_data = uijet.Resource('TimeSeries').reset(series).extractLegend();
                                legend_data.forEach(function (item, i) {
                                    item.state = series[i].state;
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
            uijet.Resource('Munis', resources.Munis);
            uijet.Resource('LatestSheet', resources.Nodes);

            this.LegendItemModel = uijet.Model();

            uijet.Resource('LegendItems', uijet.Collection({
                model       : this.LegendItemModel,
                setColors   : function () {
                    this.models.forEach(function (model, index) {
                        model.set('color', this.colors[index * 2]);
                    }, this);
                }
            }));

            uijet.Resource('ProjectState', resources.State, {
                project : 1,
                author  : 1
            });
            
            uijet.subscribe('startup', function () {
                Backbone.history.start({ root : 'static/projects/explorer/index.html' });
            });
            /*
             * Register handlers to events in UI
             */
            uijet.subscribe('viz_save.clicked', explorer.saveState);

            /*
             * Starting uijet
             */
            uijet.init({
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
        saveState   : function () {
            var chart_data = uijet.Resource('TimeSeries').toJSON(),
                selection_states = uijet.Resource('LegendItems').pluck('state'),
                state_model = uijet.Resource('ProjectState');

            chart_data.forEach(function (series, i) {
                series.state = selection_states[i];
            });
            state_model.save({ config : chart_data }, {
                success : function () {
                    explorer.router.navigate(state_model.uuid);
                },
                error   : function () {
                    console.error.apply(console, arguments);
                }
            });
        }
    };

    return explorer;
});
