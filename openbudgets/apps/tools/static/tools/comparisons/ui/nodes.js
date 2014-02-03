define([
    'uijet_dir/uijet',
    'resources'
], function (uijet) {

    uijet.Resource('NodesListState', uijet.Model({
        clearState  : function () {
            this.set({
                search      : null,
                selected    : null,
                legend_item : null,
                amount_type : null,
                selection   : null
            });
            return this;
        }
    }), {
        search      : null,
        selected    : null,
        legend_item : null,
        normalize_by: null
    });

    var clearText = function () {
        this.$content.text(gettext('Main'));
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
                'change:search'         : function (model, value) {
                    var field = 'search',
                        prev = model.previous(field),
                        was_null = prev === null;
                    if ( value === '' ) {
                        model.set(field, null, was_null && { silent : true });
                    }
                    else {
                        uijet.publish('search.changed', { args : arguments });
                    }
                },
                'change:selected'       : '-selected.changed',
                'change:normalize_by'   : function (model, key) {
                    if ( ! key  && key !== null ) {
                        model.set('normalize_by', null, { silent : true });
                        return;
                    }
                }
            },
            signals         : {
                post_wake    : 'awake'
            },
            app_events      : {
                'search_crumb_remove.clicked'       : function () {
                    this.resource.set('search', null);
                },
                'selected_crumb_remove.clicked'     : function () {
                    this.resource.set('selected', null);
                },
                'filters_selected.changed'          : function (selected) {
                    this.resource.set({ selected : selected });
                },
                'legends_list.select_state'         : function (data) {
                    this.resource.set({
                        amount_type : data.amount_type,
                        entity_id   : data.entity_id
                    })
                    .set('selection', data.selection);

                    this.wake(data);
                },
                'entities_list.selected'            : function () {
                    this.resource.clearState();
                },
                'normalization_selector.selected'   : function (key) {
                    this.resource.set('normalize_by', key);
                }
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_picker_header',
            app_events  : {
                'nodes_search.entered'  : 'wake',
                'nodes_search.cancelled': 'wake'
            }
        }
    }, {
        type    : 'Pane',
        config  : {
            element     : '#nodes_scope_name',
            signals     : {
                post_init   : function () {
                    this.$content = this.$element.find('#nodes_scope_name_content');
                }
            },
            app_events  : {
                'nodes_list.scope_changed'      : function (scope_node_model) {
                    if ( scope_node_model ) {
                        this.$content.text(scope_node_model.get('name'));
                    }
                    else {
                        clearText.call(this);
                    }
                },
                'add_legend.clicked'            : clearText,
                'legends_list.selected'         : clearText,
                'legends_list.last_deleted'     : clearText,
                'search_filter_menu.selected'   : function (data) {
                    if ( data.type === 'search' )
                        this.sleep();
                },
                'nodes_search.entered'          : 'wake',
                'nodes_search.cancelled'        : 'wake',
                'search_crumb_remove.clicked'   : 'wake'
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element : '#filters_selected',
            signals : {
                pre_click   : function () {
                    this.activated ? this.deactivate() : this.activate();
                    this.publish('changed', this.activated ? true : null);
                }
            }
        }
    }, {
        type    : 'Button',
        config  : {
            element     : '#nodes_search_exit',
            container   : 'nodes_search',
            signals     : {
                pre_click   : 'sleep'
            }
        }
    }];
});
