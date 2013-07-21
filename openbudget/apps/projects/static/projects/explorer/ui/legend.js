define([
    'uijet_dir/uijet',
    'project_widgets/LegendItem',
    'controllers/LegendsList'
], function (uijet) {

    function chartMode () {
        // reset the state of selected legend item
        this.current_index = null;
        this.$element.removeClass('picking');
        this.picking = false;
        this.resource.each(function (model) {
            model.set('disabled', false);
        });
    }

    uijet.Factory('LegendItem', {
        type    : 'LegendItem',
        config  : {
            mixins          : ['Templated'],
            template_name   : 'legend_item',
            dont_fetch      : true,
            data_events     : {
                'change:state'      : function (model, state) {
                    var count = state.selected.length;
                    this.$element.find('.selected_nodes_count').text(count);
                    uijet.publish('selected_nodes_count.updated', count);
                },
                'change:muni'       : function (model, value) {
                    this.$element.find('.entity').text(value.get('name'));
                },
                'change:color'      : function (model, color) {
                    this.setColor(color);
                },
                'change:title'      : function (model, value) {
                    uijet.publish('legend_item_title.updated', {
                        id      : model.id,
                        title   : value
                    });
                },
                'change:disabled'   : function (model, value) {
                    value ? this.disable() : this.enable();
                }
            },
            signals         : {
                post_init   : 'wake'
            }
        }
    })
    .Factory('LegendOverlay', {
        type    : 'Overlay',
        config  : {
            darken      : true,
            app_events  : {
                'add_legend.clicked'        : 'wake',
                'add_legend_cancel.clicked' : 'sleep',
                'entities_list.selected'    : 'sleep'
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
                'nodes_picker.awake'        : 'sleep',
                'welcome'                   : 'wake'
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
            data_events : {
                remove  : function () { this.resource.setColors(); },
                add     : function () { this.resource.setColors(); },
                reset   : 'resetItems'
            },
            signals     : {
                post_init   : 'createOverlay'
            },
            app_events  : {
                chart_colors            : function (colors) {
                    this.resource.colors = colors;
                },
                'legends_list.duplicate': 'addItem+',
                'legends_list.selected' : 'selectItem+',
                'legends_list.delete'   : 'removeItem+',
                'entities_list.selected': function (muni_id) {
                    this.addItem()
                        .setEntity(muni_id)
                        .updateState();
                },
                'nodes_list.selection'  : 'updateSelection+',
                'picker_done.clicked'   : chartMode,
                'chart_reset'           : chartMode,
                'legend_item_added'     : 'scroll',
                'nodes_picker.awake'    : function () {
                    this.position({ top : 0 })
                        .scroll()
                        .$element.addClass('picking');
                    this.picking = true;
                },
                'add_legend.awaking'    : function () {
                    var top = this.processed_position.top;
                    this.position({ top : top.size + (top.unit || 'px') })
                        .scroll()
                        .$element.removeClass('picking');
                    this.picking = false;
                },
                'amount_type.updated'   : function (type) {
                    this.resource.at(this.current_index).set('amount_type', type);
                }
            }
        }
    }];

});
