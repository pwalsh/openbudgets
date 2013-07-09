define([
    'uijet_dir/uijet',
    'project_widgets/TimelineChart',
    'project_widgets/Select',
    'controllers/TimelineChart'
], function (uijet) {

    uijet.Factory('ChartPeriodSelect', {
        type    : 'Select',
        config  : {
            wrapper_class   : 'chart_period_select',
            menu            : {
                mixins          : ['Templated'],
                template_name   : 'chart_period_select',
                wrapper_class   : 'chart_period_select_wrapper',
                signals         : {
                    pre_wake    : function () {
                        return false;
                    }
                },
                app_events      : {
                    'chart.fetched' : function (collection) {
                        this.setData({ periods : collection.periods() })
                            .render();
                    }
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
                }
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
            element : '#viz_duplicate'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_delete'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_export'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_publish'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#viz_save'
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#chart_heading',
            mixins      : ['Templated']
        }
    }, {
        type    : 'TimelineChart',
        config  : {
            element     : '#chart',
            adapters    : ['TimelineChart'],
            resource    : 'TimeSeries',
            style       : {
                padding : 30
            },
            data_events : {},
            app_events  : {
                'legends_list.delete'   : function () {
                    if ( this.awake ) {
                        this.render();
                    }
                }
            }
        }
    }, {
        factory : 'ChartPeriodSelect',
        config  : {
            element     : '#chart_period_start',
            menu        : {
                signals : {
                    post_render : function () {
                        this.floatPosition('top: -' + this.$wrapper[0].offsetHeight + 'px;')
                            .select(':first-child')
                            .publish('rendered');
                    }
                }
            },
            app_events  : {
                'chart_period_start_menu.rendered'  : 'wake'
            }
        }
    }, {
        factory : 'ChartPeriodSelect',
        config  : {
            element     : '#chart_period_end',
            menu        : {
                signals : {
                    post_render : function () {
                        this.floatPosition('top: -' + this.$wrapper[0].offsetHeight + 'px;')
                            .select(':last-child')
                            .publish('rendered');
                    }
                }
            },
            app_events  : {
                'chart_period_end_menu.rendered': 'wake'
            }
        }
    }];

});
