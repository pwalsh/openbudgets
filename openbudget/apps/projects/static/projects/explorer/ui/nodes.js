define([
    'uijet_dir/uijet',
    'resources',
    'ui/filters',
    'project_widgets/ClearableTextInput',
    'project_widgets/Breadcrumbs',
    'project_widgets/FilterCrumb'
], function (uijet, resources) {

    uijet.Resource('Breadcrumbs', uijet.Collection({
        model   : resources.Node
    }))
    .Resource('NodesListState', uijet.Model(), {
        search  : null,
        selected: null
    });

    var attributeNullifier = function (attr) {
            return function () {
                var obj = {};
                obj[attr] = null;
                this.resource.set(obj);
            };
        },
        nullifySearchQuery = attributeNullifier('search');

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element     : '#nodes_picker',
            position    : 'fluid',
            resource    : 'NodesListState',
            data_events : {
                'change:search'     : '-search.changed',
                'change:selected'   : '-selected.changed'
            },
            app_events  : {
                'search_crumb_remove.clicked'   : nullifySearchQuery,
                'selected_crumb_remove.clicked' : attributeNullifier('selected'),
                'filter_selected.clicked'       : function () {
                    this.resource.set({ selected : true });
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_filters_pane',
            mixins      : ['Layered'],
            position    : 'top:100 fluid',
            app_events  : {
                'nodes_search.entered'  : 'wake',
                'nodes_search.cancelled': 'wake'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#picker_done'
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
            element     : '#nodes_search',
            resource    : 'NodesListState',
            dom_events  : {
                keyup   : function (e) {
                    var code = e.keyCode || e.which,
                        value = e.target.value;
                    // enter key
                    if ( code === 13 ) {
                        value || nullifySearchQuery.call(this);
                        this.publish('entered', value || null);
                    }
                    // esc key
                    else if ( code === 27 ) {
                        nullifySearchQuery.call(this);
                        this.publish('cancelled');
                    }
                    else {
                        this.resource.set({ search : value });
                    }
                }
            },
            signals     : {
                pre_wake    : function () {
                    var initial = this.resource.get('search');
                    if ( initial === null ) {
                        initial = '';
                        this.resource.set({ search : '' });
                    }
                    this.$element.val(initial);
                },
                post_wake   : function () {
                    this.$element.focus();
                }
            },
            app_events  : {
                'nodes_search_clear.clicked': function () {
                    this.resource.set({ search : '' });
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
                'nodes_list.selected'   : function (selected) {
                    this.resource.reset(
                        uijet.Resource('LatestTemplate').branch(selected)
                    );
                }
            }
        }
    }, {
        type    : 'FilterCrumb',
        config  : {
            element     : '#search_crumb',
            dont_wake   : true,
            dom_events  : {
                click   : function () {
                    uijet.publish('filters_search.clicked');
                    this.sleep();
                }
            },
            app_events  : {
                'nodes_search.entered'  : function (query) {
                    query !== null && this.wake();
                },
                'filters_search.clicked': 'sleep',
                'search.changed'        : function (data) {
                    var query = data.args[1];
                    this.setContent(query || '');
                    query === null && this.sleep();
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#filter_selected',
            app_events  : {
                'selected.changed'  : function (data) {
                    var state = data.args[1];
                    if ( state !== null ) {
                        this.options.dont_wake = true;
                        this.sleep();
                    }
                    else {
                        this.options.dont_wake = false;
                        this.wake();
                    }
                }
            }
        }
    }, {
        type    : 'FilterCrumb',
        config  : {
            element     : '#selected_crumb',
            dont_wake   : true,
            content     : 'Selected',
            app_events  : {
                'selected.changed'  : function (data) {
                    var state = data.args[1];
                    if ( state === null ) {
                        this.options.dont_wake = true;
                        this.sleep();
                    }
                    else {
                        this.options.dont_wake = false;
                        this.wake();
                    }
                }
            }
        }
    }]);
});
