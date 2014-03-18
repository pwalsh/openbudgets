define([
    'uijet_dir/uijet',
    'composites/Select'
], function (uijet) {

    function positionNormalizationMenu () {
        var height = this.$wrapper[0].offsetHeight,
            container = uijet.$element.find('#legend_controls')[0],
            selector = this.$wrapper.parent()[0],
            container_h = container.offsetHeight,
            top = uijet.utils.getOffsetOf(selector, container).y;
        this.floatPosition('top:' + (container_h - (top + 44) < height ? -height : 44) + 'px');
    }

    return {
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
            signals     : {
                post_init   : function () {
                    this.options.content = uijet.$('#normalization_selector_selection');

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
    };
});
