define([
    'uijet_dir/uijet',
    'resources',
    'project_widgets/Breadcrumbs',
    'project_widgets/FilterCrumb'
], function (uijet, resources) {

    var closeSearchBreadcrumbsHandler = function () {
        this.$element.removeClass('searching');
    };

    return [{
        type    : 'Breadcrumbs',
        config  : {
            element     : '#items_breadcrumbs',
            mixins      : ['Templated'],
            resource    : 'Breadcrumbs',
            cloak       : true,
            dont_wake   : true,
            dont_fetch  : true,
            horizontal  : true,
            data_events : {
                reset   : 'render'
            },
            signals     : {
                post_init   : function () {
                    // reset sticky children to only the "main" breadcrumb
                    this.$original_children = this.$element.children().slice(0, 2);
                },
                pre_select  : function ($selected) {
                    return $selected.attr('data-id');
                },
                post_sleep  : closeSearchBreadcrumbsHandler
            },
            app_events  : {
                'startup'                       : function () {
                    if ( this.resource.length || window.ITEM.id ) {
                        this.wake();
                    }
                },
                'items_list.scope_changed'      : function (scope_model) {
                    var crumbs;
                    if ( scope_model ) {
                        if ( scope_model.has('ancestors') ) {
                            crumbs = scope_model.get('ancestors').slice();
                            crumbs.push(scope_model);
                        }
                        else {
                            crumbs = this.resource.slice(0, this.resource.indexOf(scope_model) + 1);
                        }
                    }
                    else {
                        crumbs = [];
                    }
                    this.resource.reset(crumbs);
                    scope_model ? this.wake() : this.sleep();
                },
                'filters_search_menu.selected'  : function () {
                    this.$element.addClass('searching');
                    this.wake();
                },
                'items_search.entered'          : closeSearchBreadcrumbsHandler,
                'items_search.cancelled'        : closeSearchBreadcrumbsHandler,
                'search_crumb_remove.clicked'   : closeSearchBreadcrumbsHandler,
                sheet_header_moved              : 'checkWrap'
            }
        }
    }, {
        type    : 'FilterCrumb',
        config  : {
            element     : '#search_crumb',
            dont_wake   : true,
            extra_class : 'hide',
            dom_events  : {
                click   : function () {
                    uijet.publish('filters_search_menu.selected', {
                        type    : 'search',
                        value   : this.$content.text()
                    });
                    this.sleep();
                }
            },
            signals     : {
                pre_wake    : function () {
                    this.$element.removeClass('hide');
                },
                pre_sleep   : function () {
                    this.$element.addClass('hide');
                }
            },
            app_events  : {
                'items_search.entered'          : function (query) {
                    if ( query !== null ) {
                        this.setContent(query);
                        this.wake();
                    }
                },
                'filters_search_menu.selected'  : function (data) {
                    if ( data.type === 'search' )
                        this.sleep();
                },
                'search_crumb_remove.clicked'   : 'sleep'
            }
        }
    }];

});
