define([
    'uijet_dir/uijet',
    'explorer'
], function (uijet, Explorer) {

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#filters',
            position: 'right:350 fluid'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#add_filter',
            position: 'top:30px'
        }
    }, {
        type    : 'List',
        config  : {
            element : '#filters_list'
        }
    }, {
        type    : 'Pane',
        config  : {
            element : '#entity_filter',
            position: 'fluid'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#entity_filter_close'
        }
    }, {
        type    : 'List',
        config  : {
            element     : '#entities_list',
            dont_wake   : true,
            mixins      : ['Templated', 'Scrolled'],
            adapters    : ['jqWheelScroll', 'Spin'],
            resource    : 'Munis',
            signals     : {
                pre_update      : 'spin',
                post_fetch_data : 'spinOff'
            },
            app_events  : {
                authenticated   : 'wake'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element : '#nodes_picker',
            position: 'fluid'
        }
    }, {
        type    : 'List',
        config  : {
            element     : '#nodes_list',
            dont_wake   : true,
            mixins      : ['Templated', 'Scrolled'],
            adapters    : ['jqWheelScroll', 'Spin'],
            resource    : 'Nodes',
            signals     : {
                pre_update      : 'spin',
                post_fetch_data : 'spinOff'
            },
            app_events  : {
                'entities_list.selected'    : function ($selected) {
                    var entity_id = $selected.attr('data-id');
                }
            }
        }
    }]);

    return Explorer;
});
