define([
    'uijet_dir/uijet',
    'composites/Select'
], function (uijet) {

    function enableMenuButton () {
        this.spinOff().enable();
    }

    uijet.Factory('ChartMenuButton', {
        type    : 'Button',
        config  : {
            extra_class     : 'hide',
            adapters        : ['Spin'],
            spinner_options : {
                lines   : 10,
                length  : 8,
                radius  : 6,
                width   : 4
            },
            signals         : {
                pre_click   : function () {
                    this.disable().spin()
                }
            },
            app_events      : {
                chart_reset : function () {
                    this.$element.removeClass('hide');  
                }
            }
        }
    });

    return [{
        type    : 'Pane',
        config  : {
            element         : '#chart_section',
            mixins          : ['Transitioned', 'Layered'],
            dont_wake       : true,
            animation_type  : 'fade',
            app_events      : {
                'picker_done.clicked'       : 'wake',
                'add_legend_cancel.clicked' : function () {
                    var has_legend_items = uijet.Resource('LegendItems').length;
                    if ( has_legend_items ) {
                        this.wake();
                    }
                    else {
                        uijet.publish('welcome');
                    }
                },
                'chart_reset'               : 'wake+'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_new'
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#viz_export',
            extra_class : 'hide',
            app_events  : {
                chart_reset : function () {
                    this.$element.removeClass('hide');  
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#viz_publish',
            extra_class : 'hide',
            app_events  : {
                chart_reset : function () {
                    this.$element.removeClass('hide');
                }
            }
        }
    }, {
        //TODO: handle state actions errors (delete/save)
        factory : 'ChartMenuButton',
        config  : {
            element     : '#viz_delete',
            app_events  : {
                state_deleted       : enableMenuButton,
                state_delete_failed : enableMenuButton,
                chart_reset         : function () {
                    if ( uijet.Resource('LoggedinUser').get('uuid') === uijet.Resource('ProjectState').get('author') ) {
                        this.$element.removeClass('hide');
                    }
                }
            }
        }
    }, {
        factory : 'ChartMenuButton',
        config  : {
            element     : '#viz_duplicate',
            app_events  : {
                state_saved         : enableMenuButton,
                state_save_failed   : enableMenuButton
            }
        }
    }, {    
        factory : 'ChartMenuButton',
        config  : {
            element     : '#viz_save',
            extra_class : '',
            app_events  : {
                state_saved         : enableMenuButton,
                state_save_failed   : enableMenuButton
            }
        }
    }];
});
