define(function () {

    return [{
        type    : 'Button',
        config  : {
            element     : '#right_edge_detector',
            click_event : 'mouseover'
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#site_menu_open',
            click_event : 'mouseover'
        }
    }, {
        type    : 'Pane',
        config  : {
            element         : '#site_menu',
            mixins          : ['Transitioned'],
            dont_wake       : true,
            animation_type  : 'slide',
            dom_events      : {
                mouseleave  : 'sleep'
            },
            app_events      : {
                'site_menu_open.clicked'        : 'wake',
                'right_edge_detector.clicked'   : 'wake',
                'site_menu_close.clicked'       : 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#site_menu_close'
        }
    }];

});
