define([
    'uijet_dir/uijet',
    'project_widgets/TimelineChart',
    'controllers/TimelineChart'
], function (uijet) {

    return [{
        type    : 'TimelineChart',
        config  : {
            element         : '#chart',
            mixins          : ['Transitioned', 'Layered'],
            adapters        : ['TimelineChart'],
            resource        : 'TimeSeries',
            dont_wake       : true,
            animation_type  : 'fade',
            style           : {
                padding : 30
            },
            data_events     : {},
            app_events      : {
                'picker_done.clicked'       : 'wake',
                'legends_list.delete'       : function () {
                    if ( this.awake ) {
                        this.render();
                    }
                },
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
    }];

});
