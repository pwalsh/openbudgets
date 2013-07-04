define([
    'uijet_dir/uijet',
    'resources',
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
        nullifySearchQuery = attributeNullifier('search'),
        clearText = function () {
            this.$element.text('');
        };

    return [{
        type    : 'Pane',
        config  : {
            element         : '#nodes_picker',
            mixins          : ['Transitioned', 'Layered'],
            dont_wake       : true,
            animation_type  : 'fade',
            resource        : 'NodesListState',
            data_events     : {
                'change:search'     : '-search.changed',
                'change:selected'   : '-selected.changed'
            },
            app_events      : {
                'search_crumb_remove.clicked'   : nullifySearchQuery,
                'selected_crumb_remove.clicked' : attributeNullifier('selected'),
                'filter_selected.clicked'       : function () {
                    this.resource.set({ selected : true });
                },
                'legends_list.change_state'     : 'wake+'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_picker_header',
//            position    : 'top:100 fluid',
            app_events  : {
                'nodes_search.entered'  : 'wake',
                'nodes_search.cancelled': 'wake'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_scope_name',
            app_events  : {
                'nodes_list.scope_changed'  : function (scope_node_model) {
                    var scope_name = scope_node_model ? scope_node_model.get('name') : '';
                    this.$element.text(scope_name);
                },
                'add_legend.clicked'        : clearText,
                'legends_list.selected'     : clearText,
                'legends_list.last_deleted' : clearText
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#filters_search'
        }
    }, {
        type    : 'ClearableTextInput',
        config  : {
            element     : '#nodes_search',
            resource    : 'NodesListState',
            dont_wake   : true,
            dom_events  : {
                keyup   : function (e) {
                    var code = e.keyCode || e.which,
                        value = e.target.value;
                    // enter key
                    if ( code === 13 ) {
                        value || nullifySearchQuery.call(this);
                        this.publish('entered', value || null)
                            .sleep();
                    }
                    // esc key
                    else if ( code === 27 ) {
                        nullifySearchQuery.call(this);
                        this.publish('cancelled')
                            .sleep();
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
                },
                'filters_search.clicked'    : 'wake'
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
                        uijet.Resource('LatestSheet').branch(selected)
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
    }, {
        type    : 'Pane',
        config  : {
            element : '#nodes_picker_footer'
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#picker_done'
        }
    }];
});
