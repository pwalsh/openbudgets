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

    var initial_crumbs,
        explorer;

    // make sure all jQuery requests (foreign and domestic) have a CSRF token 
    $(document).ajaxSend(function (event, xhr, settings) {
        if ( ! settings.headers )
            settings.headers = {};

        if ( ! ('X-CSRFToken' in settings.headers) )
            settings.headers['X-CSRFToken'] = api.getCSRFToken();
    });
    $(window).on('resize', function (e) {
        uijet.publish('app.resize', e);
    });

    // get version endpoint
    api.getVersion();

    initial_crumbs = (window.ITEM.ancestors && window.ITEM.ancestors.slice()) || [];
    if ( window.ITEM.id )
        initial_crumbs.push(window.ITEM);

    /*
     * Register resources
     */
    uijet
    .Resource('Breadcrumbs',
        uijet.Collection({
            model   : resources.Item
        }),
        initial_crumbs
    )
    .Resource('ItemsListState',
        uijet.Model(), {
            search          : null,
            sheet           : window.SHEET.id,
            period          : +window.SHEET.period,
            scope           : +window.ITEM.node || null,
            comments_item   : null
        }
    )
    .Resource('LatestSheet', resources.Items)
    .Resource('PreviousSheets', resources.Sheets)

    .Resource('ItemsListState').on('change', function (model) {
        var changed = model.changedAttributes(),
            comments_item = 'comments_item',
            item = model.get(comments_item),
            open = true;

        if ( changed ) {
            if ( 'search' in changed ) {
                uijet.publish('search.changed', changed.search);
            }

            if ( comments_item in changed ) {
                open = item;
            }
            else {
                open = false;
            }
            if ( item && ! open ) {
                // reset `comment_item` to `null`
                model.set(comments_item, null, { silent : true });
            }
            uijet.publish(open ? 'open_comments' : 'close_comments', item);
        }
    });

    if ( window.ITEM.id ) {
        // add initial item to LatestSheet
        uijet.Resource('LatestSheet').add(window.ITEM);
    }

    explorer = {
        router      : Router({
            routes  : {
                'entities/:entity/' : function (entity) {
                    this.navigate(uijet.Resource('ItemsListState').get('period') + '/', { 
                        replace : true,
                        silent  : true
                    });
                },
                'entities/:entity/:period/' : function (entity, period) {
                    uijet.Resource('ItemsListState').set({
                        period  : +period,
                        scope   : null,
                        routed  : true
                    });
                },
                'entities/:entity/:period/:uuid/' : function (entity, period, uuid) {
                    var item = uijet.Resource('LatestSheet').findWhere({ uuid : uuid }),
                        scope;

                    if ( ! item ) {
                        scope = -1;
                    }
                    else {
                        scope = +item.get('node');
                    }

                    uijet.Resource('ItemsListState').set({
                        sheet   : explorer.getSheetId(period),
                        period  : +period,
                        scope   : scope,
                        uuid    : uuid,
                        routed  : true
                    });
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
            var routes_deferred = uijet.Promise(),
                app_transition_props = {};

            explorer.routes_set_promise = routes_deferred.promise();

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
                var root = '/entities/' + window.ENTITY.slug + '/';
                explorer.routes_set_promise.then(function () {
                    Backbone.history.start({
                        pushState   : true,
                        root        : root,
                        silent      : true
                    });

                    if ( /^entities\/[^\/]+\/?$/.test(Backbone.history.getFragment()) ) {
                        explorer.router.navigate(uijet.Resource('ItemsListState').get('period') + '/', {
                            replace : true
                        });
                    }
                });
            })
            .subscribe('close_comments', function () {
                uijet.$element.removeClass('comments_open');
                app_transition_props[uijet.utils.getStyleProperty('transform')] = 'translateX(0)';
                uijet.animate(uijet.$element, app_transition_props);
            })
            .subscribe('open_comments', function ($selected_item) {
                uijet.$element.addClass('comments_open');
                app_transition_props[uijet.utils.getStyleProperty('transform')] = 'translateX(260px)';
                uijet.animate(uijet.$element, app_transition_props);
            })
            .subscribe('login', function () {
                uijet.$('.login-link')[0].click();  
            })

            /*
             * Starting uijet
             */
            .init({
                element             : '#explorer',
                templates_path      : '/static/entities/explorer/templates/',
                templates_extension : 'ms'
            });
        },
        getSheetId  : function (period) {
            return +window.ENTITY.sheets.filter(function (sheet) {
                return sheet.period == period;
            })[0].id;
        }
    };

    return explorer;
});
