define([
    'project_widgets/'
], function () {
    return [{
        type    : 'TimelineChart',
        config  : {
            element : '#chart',
            resource: 'TimeSeries'
        }
    }]
});
