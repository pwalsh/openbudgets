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
            position        : 'fluid',
            animation_type  : 'fade',
            style           : {
                padding : 30
            },
            data_events     : {},
            app_events      : {
                'picker_done.clicked'   : 'wake',
                'legends_list.delete'   : function () {
                    if ( this.awake ) {
                        this.render();
                    }
                }
            }
        }
    }];

});
