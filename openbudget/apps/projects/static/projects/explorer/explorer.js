define([
    'uijet_dir/uijet',
    'resources',
    'api',
    'modules/dom/jquery',
    'modules/pubsub/eventbox',
    'modules/promises/q',
    'modules/engine/mustache',
    'modules/xhr/jquery',
    'modules/animation/uijet-transit',
    'project_modules/uijet-search'
], function (uijet, resources, api, $, Ebox, Q, Mustache) {

    // get version endpoint
    api.getVersion();

    var Explorer = {
        start       : function (options) {
            /*
             * Get an OAuth2 token
             */
            api.auth({
                data    : options.auth,
                success : function (auth_response) {
                    // set the API's routes
                    api.getRoutes({
                        success : function (response) {
                            api._setRoutes(response);
                            uijet.publish('api_routes_set');
                        }
                    });
                    Explorer.setToken(auth_response.access_token);
                }
            });
            /*
             * Register resources
             */
            uijet.Resource('Munis', resources.Munis);
            uijet.Resource('LatestSheet', resources.Items);

            this.LegendItemModel = uijet.Model();
            uijet.Resource('LegendItems', uijet.Collection({
                model   : this.LegendItemModel
            }));
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
        } 
    };

    return Explorer;
});
