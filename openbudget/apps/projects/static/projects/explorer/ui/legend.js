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
            position    : 'top:51px left:270px',
            signals     : {
                pre_click   : 'activate'
            },
            app_events  : {
                'entities_list.selected': 'deactivate'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#legends_list',
            mixins      : ['Scrolled'],
            adapters    : ['LegendsList', 'jqWheelScroll'],
            resource    : 'LegendItems',
            position    : 'top|52px left:270px bottom',
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
                'legend_item_added'     : 'scroll'
            }
        }
    }];

});
