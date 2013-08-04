define([
    'uijet_dir/uijet',
    'resources',
    'composites/DropmenuButton',
    'composites/Select',
    'project_widgets/ClearableTextInput',
//    'project_widgets/Breadcrumbs',
    'project_widgets/FilterCrumb'
], function (uijet, resources) {

//    uijet.Resource('Breadcrumbs', uijet.Collection({
//        model   : resources.Node
//    }))
    uijet.Resource('ItemsListState', uijet.Model(), {
        search      : null,
        selected    : null,
        legend_item : null
    });

    var attributeNullifier = function (attr) {
            return function () {
                this.resource.set(attr, null);
            };
        },
        nullifySearchQuery = attributeNullifier('search'),
        clearText = function () {
            this.$content.text(gettext('Main'));
        };

    return [{
        type    : 'Pane',
        config  : {
            element     : '#sheet_scope_name',
            signals     : {
                post_init   : function () {
                    this.$content = this.$element.find('#nodes_scope_name_content');
                }
            },
            app_events  : {
                'nodes_list.scope_changed'      : function (scope_node_model) {
                    if ( scope_node_model ) {
                        this.$content.text(scope_node_model.get('name'));
                    }
                    else {
                        clearText.call(this);
                    }
                },
                'add_legend.clicked'            : clearText,
                'legends_list.selected'         : clearText,
                'legends_list.last_deleted'     : clearText,
                'filters_search_menu.selected'  : function (data) {
                    if ( data.type === 'search' )
                        this.sleep();
                },
                'nodes_search.entered'          : 'wake',
                'nodes_search.cancelled'        : 'wake',
                'search_crumb_remove.clicked'   : 'wake'
            }
        }
    }, {
        type    : 'DropmenuButton',
        config  : {
            element     : '#filters_search',
            click_event : 'mouseenter',
            dom_events  : {
                mouseleave  : function (e) {
                    this.publish('mouse_left');
                },
                click       : function () {
                    uijet.publish('filters_search_menu.selected', {
                        type: 'search'
                    });
                }
            },
            signals     : {
                pre_click   : 'cancel'
            },
            menu        : {
                mixins          : ['Templated', 'Translated'],
                float_position  : 'top: 3rem',
                dom_events      : {
                    mouseleave  : function () {
                        this.mouse_over = false;
                        this.sleep();
                    },
                    mouseenter  : function (e) {
                        this.mouse_over = true;
                    }
                },
                signals         : {
                    post_init   : function () {
                        this.prev_search_terms = [];
                    },
                    pre_wake    : function () {
                        this.context || (this.context = {});
                        this.context.prev_search_terms = this.prev_search_terms;
                    },
                    pre_select  : function ($selected) {
                        var type = $selected.attr('data-type'),
                            value;
                        if ( type === 'search' ) {
                            if ( $selected.attr('data-old') ) {
                                value = $selected.text();
                            }
                        }
                        return {
                            type    : type,
                            value   : value
                        };
                    }
                },
                app_events      : {
                    'filters_search.mouse_left' : function () {
                        this.mouse_over || this.sleep();
                    },
                    'nodes_search.entered'      : function (query) {
                        if ( query ) {
                            var index = this.prev_search_terms.indexOf(query);
                            if ( ~ index ) {
                                this.prev_search_terms.splice(index, 1);
                            }
                            this.prev_search_terms.unshift(query);
                        }
                    }
                }
            }
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element     : '#items_search',
            resource    : 'ItemsListState',
            dont_wake   : true,
            button      : {
                dont_wake   : true,
                signals     : {
                    pre_click   : 'sleep'
                },
                app_events  : {
                    'items_search.move_button'  : function (width) {
                        if ( width ) {
                            this.$element[0].style.right = width + 30 + 'px';
                            if ( ! this.awake) {
                                this.wake();
                            }
                        }
                        else if ( this.awake ) {
                            this.sleep();
                        }
                    }
                }
            },
            keys        : {
                // enter
                13          : function (e) {
                    var value = e.target.value.trim();
                    value || nullifySearchQuery.call(this);
                    this.publish('entered', value || null)
                        .sleep();
                },
                // esc
                27          : function (e) {
                    nullifySearchQuery.call(this);
                    this.publish('cancelled')
                        .sleep();
                },
                'default'   : function (e) {
                    var val = e.target.value,
                        clean = val.trim();
                    this.publish('changed', clean);
                    this.$shadow_text.text(val);
                    this.publish('move_button', val ? this.$shadow_text.width() : 0);
                    this.resource.set({ search : clean });
                }
            },
            signals     : {
                post_init   : function () {
                    this.$shadow_text = uijet.$('<span>', {
                        'class' : 'shadow_text'
                    }).prependTo(this.$wrapper);
                },
                pre_wake    : function () {
                    var initial = this.resource.get('search');
                    if ( initial === null ) {
                        initial = '';
                        this.resource.set({ search : '' });
                    }
                    this.$element.val(initial);
                    this.$shadow_text.text(initial);
                },
                post_wake   : function () {
                    var width = this.$shadow_text.width();
                    this.$element.focus();
                    if ( width ) {
                        this.publish('move_button', width);
                    }
                }
            },
            app_events  : {
                'items_search_clear.clicked'    : function () {
                    this.resource.set({ search : '' });
                },
                'filters_search_menu.selected'  : function (data) {
                    if ( data.value )
                        this.resource.set({ search : data.value });
                    if ( data.type === 'search')
                        this.wake();
                },
                'items_search_exit.clicked'     : function () {
                    nullifySearchQuery.call(this);
                    this.publish('cancelled').sleep();
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#items_search_exit',
            container   : 'items_search',
            signals     : {
                pre_click   : 'sleep'
            }
        }
//    }, {
//        type    : 'Breadcrumbs',
//        config  : {
//            element     : '#items_breadcrumbs',
//            resource    : 'Breadcrumbs',
//            data_events : {
//                change  : 'render',
//                reset   : 'render'
//            },
//            signals     : {
//                post_sleep  : function () {
//                    this.resource.reset([]);
//                }
//            },
//            app_events  : {
//                'items_list.selected'   : function (selected) {
//                    this.resource.reset(
//                        uijet.Resource('LatestSheet').branch(selected)
//                    );
//                }
//            }
//        }
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
                    query !== null && this.wake();
                },
                'filters_search_menu.selected'  : function (data) {
                    if ( data.type === 'search' )
                        this.sleep();
                },
                'search.changed'                : function (data) {
                    var query = data.args[1];
                    this.setContent(query || '');
                    query === null && this.sleep();
                }
            }
        }
    }];
});
