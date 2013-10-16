define([
    'uijet_dir/uijet',
    'widgets/Overlay',
    'composites/Select',
    'tool_widgets/LegendItem',
    'tool_mixins/Delayed',
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

    function positionNormalizationMenu () {
        var height = this.$wrapper[0].offsetHeight,
            container = uijet.$element.find('#legend_controls')[0],
            selector = this.$wrapper.parent()[0],
            container_h = container.offsetHeight,
            top = uijet.utils.getOffsetOf(selector, container).y;
        this.floatPosition('top:' + (container_h - (top + 44) < height ? -height : 44) + 'px');
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

    return [{
        type    : 'Button',
        config  : {
            element     : '#add_legend',
            signals     : {
                pre_click       : 'disable',
                pre_wake        : 'awaking',
                post_appear     : function () { this.$element.removeClass('hide'); },
                post_disappear  : function () { this.$element.addClass('hide'); }
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
    }, {
        type    : 'Select',
        config  : {
            element     : '#normalization_selector',
            dont_wake   : true,
            menu        : {
                element         : '#normalization_selector_menu',
                float_position  : 'top:44px',
                signals         : {
                    post_wake   : 'opened',
                    post_sleep  : 'closed',
                    pre_select  : function ($selected) {
                        return $selected.attr('data-key') || null;
                    }
                },
                app_events      : {
                    'app.resize'        : positionNormalizationMenu,
                    'add_legend.awaking': positionNormalizationMenu,
                    legend_item_removed : positionNormalizationMenu
                }
            },
            content     : uijet.$('#normalization_selector_selection'),
            signals     : {
                post_init   : function () {
                    uijet.Resource('ToolState')
                        .on('change:normalize_by', function (model, normalize_key) {
                            var $items = this.$element.find('.uijet_select_menu').children();
                            uijet.Resource('NodesListState').set('normalize_by', normalize_key);
                            this.setSelected(
                                normalize_key ?
                                    $items.filter('[data-key=' + normalize_key + ']') :
                                    $items.first()
                            );
                        }, this);
                }
            },
            app_events  : {
                'chart_section.awaken'              : 'wake',
                welcome                             : 'sleep',
                'nodes_picker.awake'                : 'sleep',
                'normalization_selector_menu.opened': 'activate',
                'normalization_selector_menu.closed': 'deactivate'
            }
        }
    }];

});
