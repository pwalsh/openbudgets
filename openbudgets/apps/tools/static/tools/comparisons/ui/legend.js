define(function () {

    return [{
        type    : 'Button',
        config  : {
            element     : '#add_legend',
            signals     : {
                pre_click       : 'disable',
                pre_wake        : 'awaking',
                post_appear     : function () { this.$element.removeClass('hide'); },
                post_disappear  : function () { this.$element.addClass('hide'); }
            },
            app_events  : {
                'entities_list.selected'    : 'enable',
                'add_legend_cancel.clicked' : 'enable',
                'picker_done.clicked'       : 'wake',
                'nodes_picker.awake'        : 'sleep',
                'welcome'                   : 'wake'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#add_legend_cancel',
            dont_wake   : true,
            signals     : {
                pre_click   : 'sleep'
            },
            app_events  : {
                'add_legend.clicked'    : 'wake',
                'entities_list.selected': 'sleep'
            }
        }
    }];

});
