define(function () {
    return [{
        type    : 'Pane',
        config  : {
            element         : 'header',
            mixins          : ['Templated', 'Translated'],
            resource        : 'ProjectState',
            template_name   : 'chart_heading',
            dont_fetch      : true,
            data_events     : {}
        }
    }]
});
