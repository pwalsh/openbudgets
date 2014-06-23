define([
    'uijet_dir/uijet',
    'resources',
    'project_widgets/BarChart'
], function (uijet, resources) {

    return [{
        type    : 'Pane',
        config  : {
            element         : '#bars_container',
            mixins          : ['Transitioned', 'Layered'],
            dont_wake       : true,
            animation_type  : {
                properties  : {
                    translateZ  : [0, '300px'],
                    rotateY     : [0, '-90deg'],
                    translateX  : [0, '-50%']
                },
                options     : {
                    duration: 500
                }
            },
            signals         : {
                post_wake   : 'awake'
            },
            app_events      : {
                'show_bars.clicked' : 'wake'
            }
        }
    }, {
        type    : 'BarChart',
        config  : {
            element : '#bars',
            resource: 'LatestSheet'
        }
    }];
});
