define([
    'uijet_dir/uijet',
    'widgets/Overlay',
    'composites/Select',
    'tool_widgets/LegendItem',
    'controllers/LegendsList'
], function (uijet) {

    function chartMode () {
        // reset the state of selected legend item
        this.current_model = null;
        this.$element.removeClass('picking');
        this.picking = false;
        this.resource.each(function (model) {
            model.set('disabled', false);
        });
    }

    uijet.Factory('LegendItem', {
        type    : 'LegendItem',
        config  : {
            mixins          : ['Templated', 'Translated'],
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
                'change:color'      : 'setColor',
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
                post_init       : 'wake',
                post_full_render: '-legend_item_added',
                pre_destroy     : '-legend_item_removed'
            },
            app_events      : {
                'add_legend.clicked': function () {
                    this.resource.set('disabled', true);
                }
            }
        }
    })
    .Factory('LegendOverlay', {
        type    : 'Overlay',
        config  : {
            app_events  : {
                'add_legend.clicked'        : 'wake',
                'add_legend_cancel.clicked' : 'sleep',
                'entities_list.selected'    : 'sleep'
            }
        }
    });

    return {
        type    : 'Pane',
        config  : {
            element     : '#legends_list',
            mixins      : ['Scrolled'],
            adapters    : ['LegendsList', 'jqWheelScroll'],
            resource    : 'LegendItems',
            data_events : {
                remove  : function (model) { this.resource.addColor(model.get('color')); },
                reset   : 'resetItems'
            },
            signals     : {
                post_init   : 'createOverlay'
            },
            app_events  : {
                chart_colors                : function (colors) {
                    this.resource.colors = colors;
                },
                'app.resize'                : 'sizeAndScroll',
                'legends_list.duplicate'    : 'addItem+',
                'legends_list.selected'     : 'selectItem+',
                'legends_list.delete'       : 'removeItem+',
                'entities_list.selected'    : function (muni_id) {
                    this.addItem()
                        .setEntity(muni_id)
                        .updateState();
                    uijet.utils.requestAnimFrame(
                        this.scrollTo.bind(this, this.$element.find('.legend_item:not(.disabled)'))
                    );
                },
                'nodes_list.selection'      : 'updateSelection+',
                'picker_done.clicked'       : chartMode,
                'chart_reset'               : chartMode,
                'add_legend_cancel.clicked' : chartMode,
                'legend_item_added'         : function () {
                    this.sizeAndScroll();
                    uijet.utils.requestAnimFrame(
                        this.scrollTo.bind(this, this.$element.find('.legend_item:last-child'))
                    );
                },
                'nodes_picker.awake'        : function () {
                    this.$element.addClass('picking');
                    this.picking = true;
                    this.sizeAndScroll();
                },
                'add_legend.awaking'        : function () {
                    this.$element.removeClass('picking');
                    this.picking = false;
                    this.sizeAndScroll();
                },
                'amount_type.updated'       : function (type) {
                    this.current_model.set('amount_type', type);
                }
            }
        }
    };

});
