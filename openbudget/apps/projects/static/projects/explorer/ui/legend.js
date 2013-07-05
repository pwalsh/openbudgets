define([
    'uijet_dir/uijet',
    'api',
    'project_widgets/LegendItem',
    'controllers/LegendsList'
], function (uijet, api) {

    uijet.Factory('LegendItem', {
        type    : 'LegendItem',
        config  : {
            mixins          : ['Templated'],
            template_name   : 'legend_item',
            dont_fetch      : true,
            data_events     : {
                'change:state'  : function (model, state) {
                    this.$element.find('.selected_nodes_count').text(state.selected.length);
                },
                'change:muni'   : function (model,value) {
                    this.$element.find('.entity').text(value.get('name'));
                }
            },
            signals         : {
                post_init   : 'wake'
            }
        }
    });

    return [{
        type    : 'Button',
        config  : {
            element     : '#add_legend',
            position    : 'top:44px left:277px',
            signals     : {
                pre_click   : 'disable',
                pre_wake    : 'awaking'
            },
            app_events  : {
                'entities_list.selected'    : 'enable',
                'add_legend_cancel.clicked' : 'enable',
                'picker_done.clicked'       : 'wake',
                'nodes_picker.awake'        : 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#add_legend_cancel',
            dont_wake   : true,
            signals     : {
                pre_click   : 'sleep'
            },
            app_events  : {
                'add_legend.clicked'    : 'wake',
                'entities_list.selected': 'sleep'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#legends_list',
            mixins      : ['Scrolled'],
            adapters    : ['LegendsList', 'jqWheelScroll'],
            resource    : 'LegendItems',
            position    : 'top|45px left:277px bottom',
            style       : {
                height  : 'auto'
            },
            app_events  : {
                'legends_list.duplicate': 'addItem+',
                'legends_list.selected' : 'selectItem+',
                'legends_list.delete'   : 'removeItem+',
                'entities_list.selected': function (muni_id) {
                    this.addItem()
                        .setEntity(muni_id)
                        .updateState();
                },
                'nodes_list.selection'  : 'updateSelection+',
                'picker_done.clicked'   : function () {
                    // reset the state of selected legend item
                    this.current_index = null;
                },
                'legend_item_added'     : 'scroll',
                'nodes_picker.awake'    : function () {
                    this.position({ top : 0 })
                        .scroll();
                },
                'add_legend.awaking'    : function () {
                    var top = this.processed_position.top;
                    this.position({ top : top.size + (top.unit || 'px') })
                        .scroll();
                }
            }
        }
    }];

});
