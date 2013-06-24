define([
    'uijet_dir/uijet',
    'explorer',
    'api',
    'project_widgets/ClearableTextInput',
    'project_widgets/FilteredList',
    'project_widgets/LegendItem'
], function (uijet, Explorer, api) {

    uijet.Factory('LegendItem', {
        type    : 'LegendItem',
        config  : {
            mixins          : ['Templated'],
            template_name   : 'legend_item',
            dont_fetch      : true,
            data_events     : {
                'change:items'  : function (model, value) {
                    this.$element.find('.selected_items_count').text(value.length);
                },
                'change:muni'   : function (model,value) {
                    this.$element.find('.entity').text(value.get('name'));
                }
            },
            dom_events      : {
                mouseenter  : function () {
                    this.wakeContained();
                },
                mouseleave  : function () {
                    this.sleepContained();
                }
            },
            signals         : {
                post_init   : 'wake'
            }
        }
    });


    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#legends',
            position: 'right:350 fluid'
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#legends_list',
            position    : 'fluid',
            resource    : 'LegendItems',
            signals     : {
                post_init   : function () {
                    uijet.start({
                        type    : 'Button',
                        config  : {
                            element : '#add_legend'
                        }
                    });
                }
            },
            app_events  : {
                'add_legend.clicked'    : function () {
                    var model = new Explorer.LegendItemModel({
                        title       : 'Title me',
                        description : 'Describe me',
                        muni        : '',
                        items       : []
                    });
                    this.current_index = this.resource.add(model).length - 1;

                    uijet.start({
                        factory : 'LegendItem',
                        config  : {
                            element : uijet.$('<li>', {
                                id          : this.id + '_item_' + this.current_index
                            }).appendTo(this.$element),
                            resource: model,
                            index   : this.current_index
                        }
                    }, true);
                },
                'legends_list.selected' : function (index) {
                    var model;
                    if ( index !== this.current_index ) {
                        model = this.resource.at(index);
                        this.current_index = index;
                        this.publish('change_state', {
                            entity_id   : model.get('muni').get('id'),
                            selection   : model.get('state')
                        });
                    }
                },
                'entities_list.selected': function (id) {
                    this.resource.at(this.current_index).set({
                        muni: uijet.Resource('Munis').get(id)
                    });
                },
                'items_list.selection'  : function (data) {
                    if ( data && data.reset ) return;
                    var resource = uijet.Resource('LatestSheet'),
                        selected_items = resource.where({ selected : 'selected' })
                                                 .map(uijet.Utils.prop('id')),
                        partial_items = resource.where({ selected : 'partial' })
                                                .map(uijet.Utils.prop('id'));
                    this.resource.at(this.current_index).set({
                        items   : selected_items,
                        state   : {
                            selected: selected_items,
                            partial : partial_items
                        }
                    });
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element         : '#entity_filter',
            dont_wake       : true,
            mixins          : ['Transitioned'],
            animation_type  : 'slide',
            app_events      : {
                'add_legend.clicked'            : 'wake',
                'entity_filter_close.clicked'   : 'sleep',
                'entities_list.selected'        : 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#entity_filter_close'
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element     : '#entity_field',
            button      : {
                signals : {
                    pre_click   : '-entity_field.changed'
                }
            },
            dom_events  : {
                keyup   : function (e) {
                    this.publish('changed', e.target.value);
                }
            },
            signals     : {
                post_wake   : function () {
                    this.$element.focus();
                }
            }
        }
    }, {
        type    : 'FilteredList',
        config  : {
            element     : '#entities_list',
            mixins      : ['Templated', 'Scrolled'],
            adapters    : ['jqWheelScroll', 'Spin'],
            resource    : 'Munis',
            position    : 'top|50 fluid',
            search      : {
                fields  : {
                    code    : 20,
                    name    : 10,
                    name_en : 10,
                    name_ru : 10,
                    name_ar : 10
                }
            },
            filters     : {
                search  : 'search'
            },
            signals     : {
                pre_update      : 'spin',
                post_fetch_data : function () {
                    this.spinOff()
                        .index().search_index.add( this.resource.toJSON() );
                },
                pre_wake        : function () {
                    if ( this.has_content ) {
                        return false;
                    }
                    else {
                        this.resource.url = api.getRoute('entities') + '?division__budgeting=True';
                    }
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    this.publish('rendered');
                },
                pre_select      : function ($selected) {
                    return +$selected.attr('data-id');
                }
            },
            app_events  : {
                'entity_field.changed'  : 'filterBySearch+',
                'entities_list.filtered': 'scroll'
            }
        }
    }]);

});
