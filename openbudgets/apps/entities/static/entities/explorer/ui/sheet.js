define([
    'uijet_dir/uijet',
    'resources',
    'explorer',
    'composites/DropmenuButton',
    'project_widgets/ClearableTextInput',
    'project_mixins/Delayed'
], function (uijet, resources, explorer) {

    explorer.router

        .listenTo(uijet.Resource('ItemsListState'), 'change', function (model, options) {
            var changes = model.changedAttributes(),
                navigate = false,
                period, scope, node_id;

            // sometimes search is changed to '' and then immediately and silently cleaned back to `null`
            if ( ! changes )
                return;

            if ( changes.routed ) {
                model.set('routed', false, { silent : true });
                return;
            }

            if ( 'period' in changes ) {
                navigate = true;
                period = changes.period;
            }
            else {
                period = model.get('period');
            }

            if ( 'scope' in changes ) {
                navigate = true;
                scope = changes.scope;
            }
            else {
                scope = model.get('scope');
            }

            if ( navigate ) {
                if ( scope ) {
                    node_id = scope + '/';
                }
                else {
                    node_id = '';
                }

                this.navigate(period + '/' + node_id);
            }
        });

    var attributeNullifier = function (attr) {
            return function () {
                this.resource.set(attr, null);
            };
        },
        nullifySearchQuery = attributeNullifier('search');

    return [{
        type    : 'Pane',
        config  : {
            element     : '#sheet_scope_name',
            cloak       : true,
            signals     : {
                post_init   : function () {
                    this.$content = this.$element.find('#sheet_scope_name_content');
                }
            },
            app_events  : {
                'items_list.scope_changed'      : function (scope_item_model) {
                    this.$content.text(scope_item_model ? scope_item_model.get('name') : gettext('Main'));
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
        type    : 'Button',
        config  : {
            element     : '#sheet_scope_comments',
            cloak       : true,
            signals     : {
                pre_click   : function () {
                    uijet.Resource('ItemsListState').set('comments_item', this.$element);
                }
            },
            app_events: {
                'items_list.scope_changed'  : function (scope_item_model) {
                    var has_comments = false,
                        item = '', id = '', count = '';

                    if ( scope_item_model ) {
                        item = scope_item_model.get('id');
                        id = scope_item_model.get('node');
//                        count = scope_item_model.get('comment_count');
                        has_comments = scope_item_model.get('has_comments');
                    }

                    this.$element.attr('data-item', item)
                                .attr('data-id', id)
//                                .text(count || '')
                                .text(has_comments ? '!' : '')
                                .toggleClass('has_comments', has_comments)
                                .toggleClass('hide', !has_comments);
                },
                scope_comment_created       : function (model) {
                    this.$element.text(model.get('has_comments') ? '!' : '')
                                 .toggleClass('has_comments', true);
                }
            }
        }
    }, {
        type    : 'DropmenuButton',
        config  : {
            element         : '#filters_search',
            cloak           : true,  
            click_event     : 'mouseenter',
            wrapper_class   : 'sheet_header_menu_button',
            dom_events      : {
                click       : function () {
                    this.sleep();
                    uijet.publish('filters_search_menu.selected', {
                        type: 'search'
                    });
                }
            },
            signals         : {
                post_init   : function () {
                    this.$wrapper.on('mouseleave', this.publish.bind(this, 'mouse_left'));
                },
                pre_click   : 'cancel'
            },
            menu            : {
                mixins          : ['Templated', 'Translated'],
                float_position  : 'top: 66px',
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
                        this.setContext('prev_search_terms', this.prev_search_terms);
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
                    },
                    post_select : 'sleep'
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
            },
            app_events      : {
                'items_search.entered'          : 'wake',
                'items_search.cancelled'        : 'wake',
                'filters_search_menu.selected'  : 'sleep'
            }
        }
    }, {
        type    : 'DropmenuButton',
        config  : {
            element         : '#download_sheet',
            wrapper_class   : 'sheet_header_menu_button',
            menu            : {
                element         : '#download_sheet_menu',
                float_position  : 'top: 66px',
                signals         : {
                    post_wake   : 'opened',
                    post_sleep  : 'closed'
                },
                app_events      : {
                    'sheet_selector.selected'   : function ($selected) {
                        var id = $selected.attr('data-id');
                        this.$element.find('a').each(function () {
                            var href = this.getAttribute('href');
                            this.setAttribute('href', href.replace(/sheet\/([^\/]+)/, 'sheet/' + id));
                        });
                    }
                }
            },
            app_events      : {
                'download_sheet_menu.opened': function () {
                    this.$wrapper.addClass('opened');
                },
                'download_sheet_menu.closed': function () {
                    this.$wrapper.removeClass('opened');
                }
            }
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element     : '#items_search',
            mixins      : ['Delayed'],
            resource    : 'ItemsListState',
            dont_wake   : true,
            cloak       : true,
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
                        clean = val.trim(),
                        delay = clean.length > 1 ? 500 : 1500;

                    this.publish('changed', clean);
                    this.$shadow_text.text(val);
                    this.publish('move_button', val ? this.$shadow_text.width() : 0);
                    this.instead(function (search) {
                        this.resource.set(search);
                    }, delay, { search : clean });
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
                        this.resource.set({ search : null });
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
                    this.resource.set({ search : null });
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
                },
                'search_crumb_remove.clicked'   : function () {
                    this.resource.set('search', null);
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#items_search_exit',
            container   : 'items_search',
            cloak       : true,
            signals     : {
                pre_click   : 'sleep'
            }
        }
    }];
});
