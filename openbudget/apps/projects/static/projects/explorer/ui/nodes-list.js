define([
    'uijet_dir/uijet',
    'resources',
    'ui/nodes',
    'project_widgets/FilteredList',
    'controllers/NodesList'
], function (uijet, resources) {

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element     : '#nodes_list_container',
            dont_wake   : true,
            app_events  : {
                'entities_list.selected': function (id) {
                    this.wake({ entity_id : id });
                }
            }
        }
    }, {
        type    : 'List',
        config  : {
            element     : '#nodes_list_header',
            horizontal  : true,
            position    : 'top:2rem fluid',
            signals     : {
                pre_select  : function ($selected) {
                    if ( this.$selected && $selected[0] === this.$selected[0] ) {
                        this.$selected.toggleClass('desc');
                    }
                    return {
                        column  : $selected.attr('data-column'),
                        desc    : $selected.hasClass('desc')
                    };
                }
            }
        }
    }, {
        type    : 'FilteredList',
        config  : {
            element         : '#nodes_list',
            mixins          : ['Templated', 'Scrolled'],
            adapters        : ['jqWheelScroll', 'Spin', 'NodesList'],
            resource        : 'LatestTemplate',
            position        : 'fluid',
            fetch_options   : {
                reset   : true
            },
            search          : {
                fields  : {
                    name        : 10,
                    description : 1,
                    code        : 20
                }
            },
            filters         : {
                search  : 'search',
                selected: function (state) {
                    if ( state !== null )
                        return this.resource.where({ selected : 'selected' })
                                            .map(uijet.Utils.prop('id'));
                    else
                        return null;
                }
            },
            sorting         : {
                name        : 'name',
                '-name'     : resources.utils.reverseSorting('name'),
                code        : 'code',
                '-code'     : resources.utils.reverseSorting('code'),
                direction   : 'direction',
                '-direction': resources.utils.reverseSorting('direction')
            },
            data_events     : {},
            signals         : {
                post_init       : function () {
                    this.scope = null;
                    this.active_filters = 0;
                },
                pre_wake        : function () {
                    var entity_id = this.context.entity_id,
                        selection;
                    if ( entity_id ) {
                        if ( this.latest_entity_id !== entity_id ) {
                            this.latest_entity_id = entity_id;
                            // this makes sure search index is rebuilt and view is re-rendered
                            this.scope_changed = true;
                            // this makes sure the resource will execute fetch to sync with remote server
                            this.dont_fetch = false;
                            this.resource.url = API_URL + 'templates/nodes/?page_by=2000&latest=True&entity=' + entity_id;
                        }
                        else {
                            this.dont_fetch = true;
                            this.scope_changed = false;
                            this.resetSelection(this.context.selection)
                                .publish('selection', { reset : true });
                        }
                        // change view back to main 
                        this.scope = null;
                        this.filter(this.resource.roots);
                    }
                },
                pre_update      : function () {
                    if ( ! this.has_data ) {
                        this.spin();
                        return true;
                    }
                    return false;
                },
                post_fetch_data : 'spinOff',
                pre_render      : function () {
                    if ( this.scope_changed ) {
                        if ( this.has_data ) {
                            this.scope_changed = false;
                            this.buildIndex();
                        }
                    }
                    this.has_content && this.$element.addClass('invisible');
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    if ( ! this.dont_fetch ) {
                        this.dont_fetch = true;
                        this.resetSelection(this.context.selection)
                            .publish('selection', { reset : true });
                    }
                    if ( this.active_filters ) {
                        this.filterItems();
                    }
                    else {
                        this.scroll()
                            .$element.removeClass('invisible');
                    }
                    this._finally();
                },
                pre_select      : function ($selected, e) {
                    var id = +$selected.attr('data-id');
                    if ( uijet.$(e.target).hasClass('selectbox') ) {
                        this.updateSelection(id)
                            .publish('selection');
                        return false;
                    }
                    else {
                        return ! $selected[0].hasAttribute('data-leaf') && id;
                    }
                },
                post_select     : function ($selected) {
                    var node_id = +$selected.attr('data-id') || null;
                    this.redraw(node_id);
                }
            },
            app_events      : {
                'legends_list.change_state'                 : 'wake+',
                'search.changed'                            : 'updateSearchFilter+',
                'selected.changed'                          : 'updateSelectedFilter+',
                'nodes_list.filtered'                       : function () {
                    this.scroll()
                        .$element.removeClass('invisible');
                },
                'node_breadcrumb_main.clicked'              : 'redraw',
                'node_breadcrumb_back.clicked'              : function (data) {
                    this.redraw(data.context.id);
                },
                'nodes_breadcrumbs.selected'                : 'post_select+',
                'nodes_breadcrumbs_history_menu.selected'   : 'post_select+',
                'nodes_list_header.selected'                : 'sortItems+',
                'nodes_list.selection'                      : function () {
                    var resource = this.resource,
                        filter = this.active_filters ?
                            this.resource.byAncestor :
                            this.resource.byParent; 
                    this.filter(filter.call(this.resource, this.scope));
                    if ( this.desc === false ) {
                        this.filtered.reverse();
                    }
                    this.$children.each(function (i, item) {
                        var $item = uijet.$(item),
                            id = +$item.attr('data-id'),
                            state = resource.get(id).get('selected');
                        $item.attr('data-selected', state);
                    });
                    if ( this.selected_active ) {
                        this.filterBySelected(uijet.Resource('NodesListState').get('selected'));
                    }
                }
            }
        }
    }]);

});
