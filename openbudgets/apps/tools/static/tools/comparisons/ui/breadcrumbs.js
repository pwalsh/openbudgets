define([
    'uijet_dir/uijet',
    'resources',
    'tool_widgets/Breadcrumbs'
], function (uijet, resources) {

    uijet.Resource('Breadcrumbs', uijet.Collection({
        model   : resources.Node
    }));

    var closeSearchBreadcrumbsHandler = function () {
        this.$element.removeClass('searching');
        if ( ! this.resource.length ) {
            this.sleep();
            this.$title.removeClass('hide');
        }
    };

    return {
        type    : 'Breadcrumbs',
        config  : {
            element     : '#nodes_breadcrumbs',
            mixins      : ['Templated'],
            resource    : 'Breadcrumbs',
            dont_wake   : true,
            dont_fetch  : true,
            horizontal  : true,
            data_events : {
                reset   : 'render'
            },
            signals     : {
                post_init   : function () {
                    this.$title = uijet.$('#nodes_picker_header_description');
                    // reset sticky children to only the "main" breadcrumb
                    this.$original_children = this.$element.children().slice(0, 2);
                },
                pre_wake    : function () {
                    this.resource.length && this.$title.addClass('hide');
                },
                post_sleep  : closeSearchBreadcrumbsHandler
            },
            app_events  : {
                'nodes_list.scope_changed'      : function (scope_model) {
                    var crumbs;
                    if ( scope_model ) {
                        if ( scope_model.has('ancestors') ) {
                            crumbs = scope_model.get('ancestors').slice();
                            crumbs.push(scope_model);
                        }
                        else {
                            // just slice Breadcrumbs from beginning till this scope
                            crumbs = this.resource.slice(0, this.resource.indexOf(scope_model) + 1);
                        }
                    }
                    else {
                        crumbs = [];
                    }
                    this.resource.reset(crumbs);
                    scope_model ? this.wake() : this.sleep();
                },
                'search_filter_menu.selected'   : function () {
                    this.$title.addClass('hide');
                    this.$element.addClass('searching');
                    this.wake();
                },
                'nodes_search.entered'          : closeSearchBreadcrumbsHandler,
                'nodes_search.cancelled'        : closeSearchBreadcrumbsHandler,
                'search_crumb_remove.clicked'   : closeSearchBreadcrumbsHandler
            }
        }
    };
});
