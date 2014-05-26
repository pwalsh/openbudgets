define([
    'uijet_dir/uijet',
    'resources',
    'project_widgets/ItemsSummary'
], function (uijet, resources) {

    return [{
        type    : 'ItemsSummary',
        config  : {
            element     : '#items_list_summary',
            mixins      : ['Layered'],
            signals     : {
                post_init   : function () {
                    this.$code = this.$element.find('.item_cell_code');
                    this.$direction = this.$element.find('.item_cell_direction');
                    this.$budget = this.$element.find('.item_cell_budget');
                    this.$actual = this.$element.find('.item_cell_actual');
                }
            },
            app_events  : {
                'items_list.scope_changed'  : 'renderContent+',
                'items_list.sheet_changed'  : 'renderContent+',
                'search.changed'            : function (term) {
                    if ( ! term ) {
                        this.wake();
                    }
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#results_count',
            mixins      : ['Layered'],
            dont_wake   : true,
            app_events  : {
                'items_list.filter_count'   : function (count) {
                    if ( typeof count == 'number' ) {
                        this.$element.text(interpolate(gettext('%(count)s results found'), { count : count }, true));
                        this.wake();
                    }
                }
            }
        }
    }];

});
