define(function () {
    return [{
        type    : 'Pane',
        config  : {
            element : 'footer',
            id      : 'footer',
            mixins  : ['Templated', 'Translated'],
            resource: 'ProjectState'
        }
    }]
});
