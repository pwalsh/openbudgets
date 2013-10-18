define(function () {
    return [{
        type    : 'Pane',
        config  : {
            element     : '#chart_heading',
            mixins      : ['Templated', 'Translated'],
            resource    : 'ToolState',
            dont_fetch  : true
        }
    }, {
        type    : 'List',
        config  : {
            element     : '#legend',
            mixins      : ['Templated'],
            resource    : 'TimeSeries',
            dont_fetch  : true
        }
    }]
});
