define([
    'uijet_dir/uijet',
    'resources',
    'project_widgets/ClearableTextInput',
    'project_widgets/Breadcrumbs',
    'project_widgets/FilterCrumb',
    'project_widgets/Select',
    'project_mixins/Delayed'
], function (uijet, resources) {

    uijet.Resource('Breadcrumbs', uijet.Collection({
        model   : resources.Node
    }))
    .Resource('NodesListState', uijet.Model(), {
        search      : null,
        selected    : null
    });

    var attributeNullifier = function (attr) {
            return function () {
                var obj = {};
                obj[attr] = null;
                this.resource.set(obj);
            };
        },
        nullifySearchQuery = attributeNullifier('search'),
        clearText = function () {
            this.$content.text(gettext('Main'));
        },
        amountTypeChanged = function (model, value) {
            if ( value === this.options.amount_type ) {
                this.activate().disable();
                uijet.publish('amount_type.updated', this.options.amount_type);
            }
            else {
                this.enable().deactivate();
            }
        };

    return [{
        type    : 'Pane',
        config  : {
            element         : '#nodes_picker',
            mixins          : ['Transitioned', 'Layered'],
            dont_wake       : true,
            animation_type  : 'fade',
            resource        : 'NodesListState',
            data_events     : {
                'change:search'     : '-search.changed',
                'change:selected'   : '-selected.changed'
            },
            signals         : {
                post_wake    : 'awake'
            },
            app_events      : {
                'search_crumb_remove.clicked'   : nullifySearchQuery,
                'selected_crumb_remove.clicked' : attributeNullifier('selected'),
                'filters_search_menu.selected'  : function (data) {
                    data.type === 'selected' && this.resource.set({ selected : true });
                },
                'legends_list.change_state'     : function (data) {
                    this.resource.set('amount_type', data.amount_type);
                    //TODO: on legend item adding this causes wake to be called twice and nodes_list.render is called twice
                    this.wake(data);
                },
                'entities_list.selected'        : nullifySearchQuery
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_picker_header',
            app_events  : {
                'nodes_search.entered'  : 'wake',
                'nodes_search.cancelled': 'wake'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_scope_name',
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
            mixins      : ['Delayed'],
            click_event : 'mouseover',
            dom_events  : {
                mouseout: function (e) {
                    this.instead(this.publish, 800, 'mouse_left');
                },
                click   : function () {
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
                    mouseout: function (e) {
                        var visual_target = document.elementFromPoint(e.pageX, e.pageY);
                        if ( ! this.$element[0].contains(visual_target) ) {
                            this.mouse_over = false;
                            this.sleep();
                        }
                    },
                    mouseover: function (e) {
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
            element     : '#nodes_search',
            resource    : 'NodesListState',
            dont_wake   : true,
            button      : {
                dont_wake   : true,
                signals     : {
                    pre_click   : 'sleep'
                },
                app_events  : {
                    'nodes_search.move_button'  : function (width) {
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
                'nodes_search_clear.clicked'    : function () {
                    this.resource.set({ search : '' });
                },
                'filters_search_menu.selected'  : function (data) {
                    if ( data.value )
                        this.resource.set({ search : data.value });
                    if ( data.type === 'search')
                        this.wake();
                },
                'nodes_search_exit.clicked'     : function () {
                    nullifySearchQuery.call(this);
                    this.publish('cancelled').sleep();
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#nodes_search_exit',
            container   : 'nodes_search',
            signals     : {
                pre_click   : 'sleep'
            }
        }
    }, {
        type    : 'Breadcrumbs',
        config  : {
            element     : '#nodes_breadcrumbs',
            resource    : 'Breadcrumbs',
            data_events : {
                change  : 'render',
                reset   : 'render'
            },
            signals     : {
                post_sleep  : function () {
                    this.resource.reset([]);
                }
            },
            app_events  : {
                'nodes_list.selected'   : function (selected) {
                    this.resource.reset(
                        uijet.Resource('LatestSheet').branch(selected)
                    );
                }
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
                'nodes_search.entered'          : function (query) {
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
                },
                'nodes_picker.awake'            : function () {
                    if ( uijet.Resource('NodesListState').get('search') ) {
                        this.wake();
                    }
                }
            }
        }
    }, {
        type    : 'FilterCrumb',
        config  : {
            element     : '#selected_crumb',
            dont_wake   : true,
            content     : gettext('Selected'),
            app_events  : {
                'selected.changed'  : function (data) {
                    var state = data.args[1];
                    if ( state === null ) {
                        this.options.dont_wake = true;
                        this.sleep();
                    }
                    else {
                        this.options.dont_wake = false;
                        this.wake();
                    }
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element : '#nodes_picker_footer'
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#summarize_budget',
            resource    : 'NodesListState',
            amount_type : 'budget',
            data_events : {
                'change:amount_type': amountTypeChanged
            },
            signals     : {
                pre_click   : function () {
                    if ( ! this.activated ) {
                        this.resource.set('amount_type', 'budget');
                    }
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#summarize_actual',
            resource    : 'NodesListState',
            amount_type : 'actual',
            data_events : {
                'change:amount_type': amountTypeChanged
            },
            signals     : {
                pre_click   : function () {
                    if ( ! this.activated ) {
                        this.resource.set('amount_type', 'actual');
                    }
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#picker_done',
            app_events  : {
                'entities_list.selected'        : 'disable',
                'legends_list.delete'           : 'enable',
                'selected_nodes_count.updated'  : function (count) {
                    count ? this.enable() : this.disable();
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#results_count',
            dont_wake   : true,
            app_events  : {
                'nodes_list.filter_count'   : function (count) {
                    if ( typeof count == 'number' ) {
                        this.$element.text(interpolate(gettext('%(count)s results found'), { count : count }, true));
                        this.wake();
                    }
                },
                'search.changed'            : function (data) {
                    if ( ! data.args[1] && ! data.args[0].get('selected') ) {
                        this.sleep();
                    }
                },
                'selected.changed'          : function (data) {
                    if ( ! data.args[1] && ! data.args[0].get('search') ) {
                        this.sleep();
                    }
                }
            }
        }
    }];
});
