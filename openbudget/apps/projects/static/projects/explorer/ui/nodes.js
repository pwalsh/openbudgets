define([
    'uijet_dir/uijet',
    'resources',
    'project_widgets/ClearableTextInput',
    'project_widgets/Breadcrumbs'
], function (uijet, resources) {

    uijet.Resource('Breadcrumbs', uijet.Collection({
        model   : resources.Node
    }));

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#nodes_picker',
            position: 'fluid'
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_filters_pane',
            mixins      : ['Layered'],
            position    : 'top:100 fluid',
            app_events  : {
                'nodes_search.exited'   : 'wake+'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#filters_done'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#filters_search'
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_search_pane',
            mixins      : ['Layered'],
            dont_wake   : true,
            position    : 'top:100 fluid',
            app_events  : {
                'filters_search.clicked': 'wake'
            }
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element : '#nodes_search',
            button      : {
                signals : {
                    pre_click   : '-nodes_search.changed'
                }
            },
            dom_events  : {
                keyup   : function (e) {
                    var code = e.keyCode || e.which,
                        value = e.target.value;
                    // enter key
                    if ( code === 13 ) {
                        this.publish('exited', value)
                    }
                    // esc key
                    else if ( code === 27 ) {
                        this.publish('exited', '');
                    }
                    else {
                        this.publish('changed', value);
                    }
                }
            },
            signals     : {
                post_wake   : function () {
                    this.$element.focus();
                }
            }
        }
    }, {
        type    : 'Breadcrumbs',
        config  : {
            element     : '#nodes_breadcrumbs',
            resource    : 'Breadcrumbs',
            data_events : {
                change  : 'render',
                reset   : 'render'
            },
            app_events  : {
                'nodes_list.ready'      : function () {},
                'nodes_list.selected'   : function (selected) {
                    this.resource.reset(
                        uijet.Resource('LatestTemplate').branch(selected)
                    );
                }
            }
        }
    }]);
    
});
