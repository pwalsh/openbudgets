define([
    'uijet_dir/uijet',
    'tool_widgets/FilterCrumb'
], function (uijet) {

    return {
        type    : 'FilterCrumb',
        config  : {
            element     : '#search_crumb',
            dont_wake   : true,
            extra_class : 'hide',
            dom_events  : {
                click   : function () {
                    uijet.publish('search_filter_menu.selected', {
                        type    : 'search',
                        value   : this.$content.text()
                    });
                    this.sleep();
                }
            },
            signals     : {
                pre_wake    : function () {
                    this.$element.removeClass('hide');
                },
                pre_sleep   : function () {
                    this.$element.addClass('hide');
                }
            },
            app_events  : {
                'nodes_search.entered'          : function (query) {
                    query !== null && this.wake();
                },
                'search_filter_menu.selected'   : function (data) {
                    if ( data.type === 'search' )
                        this.sleep();
                },
                'search.changed'                : function (data) {
                    var query = data.args[1];
                    this.setContent(query || '');
                    query === null && this.sleep();
                },
                'nodes_picker.awake'            : function () {
                    if ( uijet.Resource('NodesListState').get('search') ) {
                        this.wake();
                    }
                }
            }
        }
    };

});
