define([
    'uijet_dir/uijet',
    'resources',
    'modules/dom/jquery',
    'modules/pubsub/eventbox',
    'modules/promises/q',
    'modules/engine/mustache',
    'modules/xhr/jquery',
    'modules/animation/uijet-transit',
    'project_modules/uijet-search'
], function (uijet, resources, $, Ebox, Q, Mustache) {
    var Explorer = {
        start       : function (options) {
            /*
             * Get an OAuth2 token
             */
            uijet.xhr(options.AUTH_URL, {
                type    : 'POST',
                data    : options.auth
            })
            .then(function (response) {
                Explorer.setToken(response.access_token);
            }, function (xhr) {
                console.error('Auth failed!', xhr);
            });
            /*
             * Register resources
             */
            uijet.Resource('Munis', resources.Munis);
            uijet.Resource('LatestTemplate', resources.Nodes);

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
