define([
    'uijet_dir/uijet',
    'api',
    'comparisons',
    'tool_widgets/ClearableTextInput',
    'tool_widgets/FilteredList'
], function (uijet, api, comparisons) {

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
                    var val = e.target.value,
                        clean = val.trim();
                    this.publish('changed', clean);
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
            promise         : comparisons.routes_set_promise,
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
            data_events     : {
                'change:selected'   : function () {
                    uijet.Resource('Contexts').fetch({
                        data: {
                            entities: this.resource.where({ selected : true }).map(function (model) {
                                return model.id;
                            }).toString()
                        },
                        remove  : false
                    });
                }
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
                    if ( this.queued_filters ) {
                        this.publish('rendered');
                        setImmediate(this.filterChildren.bind(this));
                    }
                },
                pre_select      : function ($selected) {
                    var id = +$selected.attr('data-id');
                    this.resource.get(id).set('selected', true);
                    return id;
                },
                post_filtered   : function (ids) {
                    var search_term = this.last_search_term;
                    uijet.utils.requestAnimFrame( function () {
                        var resource = this.resource,
                            highlight = this.highlight.bind(this);
                        if ( this.$last_filter_result ) {
                            this.$last_filter_result.each(function (i, item) {
                                var text = resource.get(item.getAttribute('data-id')).get('name');
                                if ( search_term ) {
                                    item.innerHTML = highlight(text, search_term);
                                }
                                else {
                                    item.innerHTML = '';
                                    item.appendChild(document.createTextNode(text));
                                }
                            });
                        }
                    }.bind(this) );
                }
            },
            app_events      : {
                'entity_field.changed'  : function (value) {
                    this.last_search_term = value || null;
                    this.filterBySearch(this.last_search_term);
                    if ( ! this.queued_filters ) {
                        this.filterChildren();
                        uijet.utils.requestAnimFrame(this.scroll.bind(this));
                    }
                }
            }
        }
    }];

});
