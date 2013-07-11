define([
    'uijet_dir/uijet'
], function (uijet) {

    return [{
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
            app_events      : {
                'site_menu_open.clicked'    : 'wake',
                'site_menu_close.clicked'   : 'sleep'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#site_menu_close'
        }
    }];

});
