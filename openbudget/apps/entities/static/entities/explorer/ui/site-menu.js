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
            element         : '#panel-nav',
            mixins          : ['Transitioned'],
            dont_wake       : true,
            animation_type  : 'slide',
            dom_events      : {
                mouseleave  : 'sleep'
            },
            app_events      : {
                'site_menu_open.clicked'        : 'wake',
                'right_edge_detector.clicked'   : 'wake',
                'panel-nav-close.clicked'       : 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#panel-nav-close'
        }
    }];

});
