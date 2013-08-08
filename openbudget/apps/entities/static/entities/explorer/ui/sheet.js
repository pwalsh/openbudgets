define([
    'uijet_dir/uijet',
    'resources',
    'explorer',
    'composites/DropmenuButton',
    'composites/Select',
    'project_widgets/ClearableTextInput',
    'project_widgets/FilterCrumb'
], function (uijet, resources, explorer) {

    uijet.Resource('Breadcrumbs', uijet.Collection({
        model   : resources.Item
    }))
    .Resource('ItemsListState', uijet.Model(), {
        search  : null,
        sheet   : window.SHEET.id,
        period  : window.SHEET.period
    });

    var state_model = uijet.Resource('ItemsListState');

    explorer.router
        .listenTo(state_model, 'change:scope', function (model, value) {
            var uuid = value ?
                uijet.Resource('LatestSheet').findWhere({ node : value }).get('uuid') + '/' :
                '';
            this.navigate(state_model.get('period') + '/' + uuid);
        })
        .listenTo(state_model, 'change:period', function (model, value) { 
            this.navigate(value + '/');
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
        type    : 'Select',
        config  : {
            element     : '#sheet_selector',
            resource    : 'ItemsListState',
            menu        : {
                element         : '#sheet_selector_menu',
                float_position  : 'top:44px',
                initial         : '[data-id=' + window.SHEET.id + ']',
                signals         : {
                    post_wake   : 'opened',
                    post_sleep  : 'closed'
                }
            },
            content     : uijet.$('#sheet_selector_content'),
            sync        : true,
            data_events : {
                'change:period'  : function (model, period) {
                    var id = window.ENTITY.sheets.filter(function (sheet) {
                            return sheet.period == period;
                        })[0].id;
                    this.select(this.$element.find('[data-id=' + id + ']'));
                }
            },
            signals     : {
                post_select : function ($selected) {
                    this.resource.set({
                        sheet   : +$selected.attr('data-id'),
                        period  : $selected.text()  
                    });
                }
            },
            app_events  : {
                'sheet_selector_menu.opened': 'activate',
                'sheet_selector_menu.closed': 'deactivate'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#sheet_scope_name',
            signals     : {
                post_init   : function () {
                    this.$content = this.$element.find('#sheet_scope_name_content');
                }
            },
            app_events  : {
                'items_list.scope_changed'      : function (scope_item_model) {
                    if ( scope_item_model ) {
                        this.$content.text(scope_item_model.get('name'));
                    }
                    else {
                        clearText.call(this);
                    }
                },
                'filters_search_menu.selected'  : function (data) {
                    if ( data.type === 'search' )
                        this.sleep();
                },
                'items_search.entered'          : 'wake',
                'items_search.cancelled'        : 'wake',
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
                    'items_search.entered'      : function (query) {
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
    }, {
        type    : 'List',
        config  : {
            element     : '#items_breadcrumbs',
            mixins      : ['Templated'],
            resource    : 'Breadcrumbs',
            dont_wake   : true,
            dont_fetch  : true,
            horizontal  : true,
            data_events : {
                reset   : 'render'
            },
            signals     : {
                post_wake   : function () {
                    return false;
                },
                pre_select  : function ($selected) {
                    return +$selected.attr('data-id');
                }
            },
            app_events  : {
                'items_list.scope_changed'  : function (scope_model) {
                    var ancestors = scope_model ?
                        scope_model.get('ancestors') :
                        [];
                    this.resource.reset(ancestors);
                    scope_model ? this.wake() : this.sleep();
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
