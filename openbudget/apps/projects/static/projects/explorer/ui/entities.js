define([
    'uijet_dir/uijet',
    'api',
    'explorer',
    'project_widgets/ClearableTextInput',
    'project_widgets/FilteredList'
], function (uijet, api, explorer) {

    return [{
        type    : 'Pane',
        config  : {
            element         : '#entity_selection',
            dont_wake       : true,
            mixins          : ['Transitioned', 'Layered'],
            animation_type  : 'fade',
            app_events      : {
                'add_legend.clicked'        : 'wake',
                'add_legend_cancel.clicked' : 'sleep',
                'entities_list.selected'    : 'sleep'
            }
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element     : '#entity_field',
            button      : {
                dont_wake   : true,
                signals     : {
                    pre_click   : function () {
                        uijet.publish('entity_field.changed');
                        this.sleep();
                    }
                },
                app_events  : {
                    'entity_field.move_button'  : function (width) {
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
            dom_events  : {
                keyup   : function (e) {
                    var val = e.target.value;
                    this.publish('changed', e.target.value);
                    this.$shadow_text.text(val);
                    this.publish('move_button', val ? this.$shadow_text.width() : 0);
                }
            },
            signals     : {
                post_init   : function () {
                    this.$shadow_text = uijet.$('<span>', {
                        'class' : 'shadow_text'
                    }).prependTo(this.$wrapper);
                },
                post_wake   : function () {
                    var width = this.$shadow_text.width();
                    this.$element.focus();
                    if ( width ) {
                        this.publish('move_button', width);
                    }
                }
            }
        }
    }, {
        type    : 'FilteredList',
        config  : {
            element         : '#entities_list',
            mixins          : ['Templated', 'Scrolled', 'Deferred'],
            adapters        : ['jqWheelScroll', 'Spin'],
            resource        : 'Munis',
            promise         : explorer.routes_set_promise,
            position        : 'top|120px bottom fluid',
            fetch_options   : {
                data: {
                    has_sheets  : true,
                    page_by     : 300,
                    ordering    : 'name'
                }
            },
            search          : {
                fields  : {
                    code    : 20,
                    name    : 10,
                    name_en : 10,
                    name_ru : 10,
                    name_ar : 10
                }
            },
            filters         : {
                search  : 'search'
            },
            signals         : {
                pre_wake        : function () {
                    return ! this.has_content;
                },
                pre_update      : 'spin',
                post_fetch_data : function () {
                    this.spinOff()
                        .index().search_index.add( this.resource.toJSON() );
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    this.publish('rendered');
                },
                pre_select      : function ($selected) {
                    return +$selected.attr('data-id');
                }
            },
            app_events      : {
                'entity_field.changed'  : 'filterBySearch+',
                'entities_list.filtered': 'scroll'
            }
        }
    }];

});
