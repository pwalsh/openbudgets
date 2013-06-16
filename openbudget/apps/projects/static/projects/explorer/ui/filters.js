define([
    'uijet_dir/uijet',
    'explorer',
    'project_widgets/ClearableTextInput',
    'project_widgets/FilteredList',
    'project_widgets/LegendItem'
], function (uijet, Explorer) {

    uijet.Factory('LegendItem', {
        type    : 'LegendItem',
        config  : {
            mixins          : ['Templated'],
            template_name   : 'legend_item',
            signals         : {
                post_init   : 'wake',
                pre_update  : function () { return false; }
            },
            app_events      : {
                'entities_list.selected': function (id) {
                    this.resource.set({
                        muni : uijet.Resource('Munis').get(id)
                    });
                }
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
        type    : 'Button',
        config  : {
            element : '#add_legend',
            position: 'top:50px fluid'
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#legends_list',
            position    : 'fluid',
            resource    : 'LegendItems',
            app_events  : {
                'add_legend.clicked'    : function () {
                    var model = new Explorer.LegendItemModel({
                        title       : 'Title me',
                        description : 'Describe me',
                        muni        : '',
                        nodes       : []
                    });
                    this.current_index = this.resource.add(model).length - 1;

                    uijet.start({
                        factory : 'LegendItem',
                        config  : {
                            element : uijet.$('<li>', {
                                id  : this.id + '_item_' + this.current_index
                            }).appendTo(this.$element),
                            resource: model
                        }
                    }, true);
                },
                'nodes_list.selection'  : function () {
                    var nodes = uijet.Resource('LatestTemplate')
                                        .where({ selected : 'selected' })
                                        .map(uijet.Utils.prop('id'));
                    this.resource.at(this.current_index).set({
                        nodes   : nodes
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
                'entity_filter_close.clicked'   : 'sleep'
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
                    return ! this.has_content;
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
