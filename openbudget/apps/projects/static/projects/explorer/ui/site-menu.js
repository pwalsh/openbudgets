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
            dom_events      : {
                mouseout: function (e) {
                    if ( ! this.$element[0].contains(document.elementFromPoint(e.pageX, e.pageY)) ) {
                        this.sleep();
                    }
                }
            },
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
