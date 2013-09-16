define([
    'project_widgets/TimelineChart',
    'controllers/TimelineChart'
], function () {

    return [{
        type    : 'TimelineChart',
        config  : {
            element : '#chart',
            adapters: ['TimelineChart'],
            resource: 'TimeSeries',
            style   : {
                padding : '20px 20px 0'
            },
            signals : {
                pre_render  : '_draw'
            }
        }
    }];

});
