define([
    'uijet_dir/uijet'
], function (uijet) {

    return [{
        type    : 'Pane',
        config  : {
            element     : '#items_comments_container',
            mixins      : ['Scrolled', 'Transitioned'],
            adapters    : ['jqWheelScroll']
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#items_comments_close',
            dont_wake   : true,
            signals     : {
                pre_click   : 'sleep'
            },
            app_events  : {
                'open_comments' : 'wake'
            }
        }
    }];
});
