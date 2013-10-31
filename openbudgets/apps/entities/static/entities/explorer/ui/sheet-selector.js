define([
    'uijet_dir/uijet',
    'explorer',
    'resources',
    'composites/Select',
], function (uijet, explorer) {
    
    return {
        type    : 'Select',
        config  : {
            element     : '#sheet_selector',
            resource    : 'ItemsListState',
            menu        : {
                element         : '#sheet_selector_menu',
                float_position  : 'top:44px',
                initial         : '[data-id=' + window.SHEET.id + ']',
                signals         : {
                    post_wake   : 'opened',
                    post_sleep  : 'closed'
                }
            },
            content     : uijet.$('#sheet_selector_content'),
            sync        : true,
            data_events : {
                'change:period'  : function (model, period) {
                    var id = explorer.getSheetId(period);
                    this.select(this.$element.find('[data-id=' + id + ']'));
                }
            },
            signals     : {
                post_select : function ($selected) {
                    this.resource.set({
                        sheet   : $selected.attr('data-id'),
                        period  : +$selected.text()
                    });
                }
            },
            app_events  : {
                'sheet_selector_menu.opened'    : 'activate',
                'sheet_selector_menu.closed'    : 'deactivate',
                'filters_search_menu.selected'  : 'sleep',
                'items_search.entered'          : 'wake',
                'items_search.cancelled'        : 'wake',
                'search_crumb_remove.clicked'   : 'wake'
            }
        }
    };

});
