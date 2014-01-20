define([
    'uijet_dir/uijet',
    'resources',
    'tool_widgets/FilteredList',
    'controllers/NodesList'
], function (uijet, resources) {

    uijet.Resource('NodesSearchResult', resources.Nodes);

    return [{
        type    : 'List',
        config  : {
            element     : '#nodes_list_header',
            horizontal  : true,
            position    : 'top:27px fluid',
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
        type    : 'List',
        config  : {
            element         : '#nodes_list',
            mixins          : ['Templated', 'Scrolled'],
            adapters        : ['jqWheelScroll', 'Spin', 'NodesList'],
            resource        : 'LatestSheet',
            position        : 'fluid',
            fetch_options   : {
                remove  : false,
                cache   : true,
                merge   : false,
                expires : 8 * 3600,
                data    : {
                    page_by : 4000,
                    parents : 'none'
                }
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
                    //TODO: copy-pasted from old nodes_list, need to rewrite
                    if ( state === true )
                        return this.resource.where({ selected : 'selected' })
                                            .map(uijet.utils.prop('id'));
                    else
                        return null;
                }
            },
            sorting         : {
                name        : 'name',
                '-name'     : resources.utils.reverseSorting('name'),
                code        : resources.utils.nestingSort,
                '-code'     : resources.utils.reverseNestingSort,
                direction   : 'direction',
                '-direction': resources.utils.reverseSorting('direction')
            },
            data_events     : {
                request : function (resource, xhr, options) {
                    if ( this.last_request && this.last_request.state() == 'pending' ) {
                        this.last_request.abort();
                    }
                    this.last_request = xhr;
                },
                reset   : function () {
                    this.has_data = true;
                    delete this.$original_children;
                }
            },
            signals         : {
                post_init       : function () {
                    var state_model = uijet.Resource('NodesListState');

                    this.scope = null;
                    this.index();

                    this.listenTo(state_model, 'change', function (model, options) {
                        var changed = model.changedAttributes(),
                            search = null,
                            entity_id, scope,
                            prev, prev_templates, prev_template;

                        if ( ! changed )
                            return;

                        if ( 'search' in changed ) {
                            search = model.get('search');
                            if ( ! search ) {
                                prev = state_model.previous('search');
                                if ( ! prev ) {
                                    state_model.set('search', null, { silent : true });
                                    return;
                                }
                            }
                        }

                        if ( 'selection' in changed ) {
                            //TODO: this was copy-pasted from old nodes_list, need to check and fix
                            if ( this.has_data ) {
                                this.resetSelection(changed.selection)
                                    .publish('selection', { reset : true });
                            }
                            else {
                                this.reselect = true;
                            }
                        }

                        if ( 'entity_id' in changed ) {
                            prev = model.previous('entity_id');

                            // make sure we cache the previous template
                            if ( prev ) {
                                prev_templates = uijet.Resource('PreviousSheets');

                                // assigning in purpose to reuse as previous template
                                if ( prev_template = prev_templates.get(prev) ) {
                                    // update cache of previous Nodes collection with current LatestSheet state
                                    prev_template.get('nodes').set(this.resource.models, { remove : false });
                                }
                                else {
                                    prev_templates.add({
                                        id      : prev,
                                        nodes   : this.resource.clone()
                                    });
                                }
                            }
                            entity_id = model.get('entity_id');
                        }
                        else if ( 'scope' in changed ) {
                            scope = model.get('scope');
                        }
                        else if ( ! ('search' in changed) ) {
                            // move along people, nothing to see here
                            return;
                        }

                        this._finally().wake({
                            entity_id   : entity_id,
                            search      : search,
                            scope       : scope === void 0 ? model.get('scope') : scope || null
                        });
                    });
                },
                pre_wake        : function () {
                    // usually on first load when there's no context, just bail out
                    if ( ! this.context ) return false;

                    var state = uijet.Resource('NodesListState'),
                        undef = void 0,
                        scope = 'scope' in this.context ? this.context.scope || null : undef,
                        entity_id = this.context.entity_id,
                        search = this.context.search || state.get('search'),
                        fetch_ops_data = this.options.fetch_options.data,
                        prev_template;

                    if ( entity_id ) {
                        if ( prev_template = uijet.Resource('PreviousSheets').get(entity_id) ) {
                            this.resource = prev_template.get('nodes');
                            // register current collection as the new instance
                            uijet.Resource('LatestSheet', this.resource, true);
                            scope = scope === -1 ?
                                this.resource.findWhere(state.get('scope')).get('id') :
                                scope;
                        }
                        else {
                            // instantiate a new collection
                            this.resource = new resources.Nodes();
                            // register it
                            uijet.Resource('LatestSheet', this.resource, true);
                        }
                    }
                    // if for some reason scope is still unknown reset it to `null`
                    if ( scope === -1 ) {
                        scope = null;
                    }

                    this.search_active = !!search;

                    delete this.filtered;
                    this.has_data = false;

                    if ( entity_id ) {
                        this.template_changed = true;
                        fetch_ops_data.entity_id = entity_id;
                    }

                    if ( search ) {
                        fetch_ops_data.search = search;
                        delete fetch_ops_data.parents;
                    }
                    else {
                        delete fetch_ops_data.search;
                        fetch_ops_data.parents = (scope === undef ? this.scope : scope) || 'none';
                    }

                    // set scope if it's defined in the context
                    scope !== undef && this.setScope(scope);
                },
                pre_update      : 'spin',
                post_fetch_data : function (response) {
                    var scope_changed = this.scope_changed;
                    // after we had to reset because of entity change make sure turn reset off again
                    if ( this.options.fetch_options.reset ) {
                        this.options.fetch_options.reset = false;
                    }
                    if ( this.search_active ) {
                        this.filter(uijet.Resource('NodesSearchResult')
                            .reset(response.results)
                            .byAncestor(this.scope));
                    }
                    else {
                        this.filter(this.resource.byParent, this.scope);
                    }

                    if ( scope_changed ) {
                        this.scope_changed = false;
                        this._publishScope();
                    }
                    if ( this.template_changed ) {
                        this.template_changed = false;
//                        scope_changed || this.publish('sheet_changed', null);
                    }

                    this.spinOff();
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    if ( this.search_active ) {
                        var search_term = uijet.Resource('NodesListState').get('search');

                        this.publish('filter_count', this.$children.length)
                            ._prepareScrolledSize();

                        uijet.utils.requestAnimFrame( this.toggleHighlight.bind(this, search_term) );
                        uijet.utils.requestAnimFrame( this.scroll.bind(this) );
                    }
                    else {
                        this.scroll();
                    }

                    this._finally();
                },
                pre_select      : function ($selected, event) {
                    var id = $selected.attr('data-id');
                    if ( uijet.$(event.target).hasClass('selectbox') ) {
                        this.updateSelection(id)
                            .publish('selection');
                        return false;
                    }
                    else {
                        return ! $selected[0].hasAttribute('data-leaf') && id;
                    }
                },
                post_select     : function ($selected) {
                    uijet.Resource('NodesListState').set('scope', $selected.attr('data-id'));
                }
            },
            app_events      : {
                'nodes_breadcrumbs.selected': 'post_select+',
                'nodes_list_header.selected': 'sortItems+',
                'picker_done.clicked'       : function () {
                    /*
                     * Make sure that every time we hit "done" we cache current template state
                     * in `PreviousSheets` resource.
                     */
                    var prev_templates = uijet.Resource('PreviousSheets'),
                        entity_id = uijet.Resource('NodesListState').get('entity_id'),
                        prev_template;
                    if ( prev_template = prev_templates.get(entity_id) ) {
                        prev_template.get('nodes').set(this.resource.models, { remove : false });
                    }
                    else {
                        prev_templates.add({
                            id: entity_id,
                            nodes: this.resource.clone()
                        });
                    }
                },
                'nodes_list.selection'      : function () {
                    var resource = this.resource;
                    //update DOM with collection's state
                    this.$children.each(function (i, node) {
                        var $node = uijet.$(node),
                            id = $node.attr('data-id'),
                            state = resource.get(id).get('selected');
                        $node.attr('data-selected', state);
                    });
                }
            }
        }
//    }, {
//        type    : 'FilteredList',
//        config  : {
//            element         : '#nodes_list',
//            mixins          : ['Templated', 'Scrolled'],
//            adapters        : ['jqWheelScroll', 'Spin', 'NodesList'],
//            resource        : 'LatestSheet',
//            position        : 'fluid',
//            fetch_options   : {
//                reset   : true,
//                cache   : true,
//                expires : 8 * 3600,
//                data    : {
//                    page_by : 4000,
//                    latest  : 'True'
//                }
//            },
//            search          : {
//                fields  : {
//                    name        : 10,
//                    description : 1,
//                    code        : 20
//                }
//            },
//            filters         : {
//                search  : 'search',
//                selected: function (state) {
//                    if ( state === true )
//                        return this.resource.where({ selected : 'selected' })
//                                            .map(uijet.utils.prop('id'));
//                    else
//                        return null;
//                }
//            },
//            sorting         : {
//                name        : 'name',
//                '-name'     : resources.utils.reverseSorting('name'),
//                code        : resources.utils.nestingSort,
//                '-code'     : resources.utils.reverseNestingSort,
//                direction   : 'direction',
//                '-direction': resources.utils.reverseSorting('direction')
//            },
//            data_events     : {},
//            signals         : {
//                post_init       : function () {
//                    var state_model = uijet.Resource('NodesListState');
//
//                    state_model.on('change:entity_id', function (model, entity_id) {
//                        this.dont_fetch = false;
//                        this.has_data = false;
//                        this.rebuild_index = true;
//                        this.options.fetch_options.data.entity = entity_id;
//                    }, this);
//
//                    state_model.on('change:selection', function (model, selection) {
//                        if ( this.has_data ) {
//                            this.resetSelection(selection)
//                                .publish('selection', { reset : true });
//                        }
//                        else {
//                            this.reselect = true;
//                        }
//                    }, this);
//                },
//                pre_wake        : function () {
                    //usually on first load when there's no context, just bail out
//                    if ( ! this.context ) return false;
//
//                    if ( this.context.entity_id ) {
                        //change view back to main
//                        this.setScope(null);
//
//                        var state = uijet.Resource('NodesListState');
//                        this.updateFlags(state.attributes);
//
//                        if ( this.active_filters ) {
//                            this.filter(this.resource.byAncestor)
//                        }
//                        else {
//                            this.filter(this.resource.roots);
//                        }
//                    }
//                    else {
//                        console.error('Nodes list started without a given entity ID.', this.context);
//                    }
//                },
//                pre_update      : 'spin',
//                post_fetch_data : function () {
//                    if ( this.queued_filters ) {
//                        this.queued_filters = false;
//                        this.filter(this.resource.byAncestor);
//                    }
//                    if ( this.reselect ) {
//                        this.reselect = false;
//                        this.resetSelection(this.context.selection);
//                    }
//                    if ( this.rebuild_index ) {
                        //clear FilterList's cache
//                        this.rebuild_index = false;
//                        this.cached_results = {};
//                        this.$last_filter_result = null;
                        //rebuild index
//                        this.buildIndex();
//                    }
//                    this.spinOff();
//                },
//                post_render     : function () {
//                    this.$children = this.$element.children();
//                    if ( this.active_filters ) {
//                        this.filterChildren();
//                    }
//                    else {
//                        this.scroll();
//                    }
//
//                    this._finally();
//                },
//                pre_select      : function ($selected, e) {
//                    var id = $selected.attr('data-id');
//                    if ( uijet.$(e.target).hasClass('selectbox') ) {
//                        this.updateSelection(id)
//                            .publish('selection');
//                        return false;
//                    }
//                    else {
//                        return ! $selected[0].hasAttribute('data-leaf') && id;
//                    }
//                },
//                post_select     : function ($selected) {
//                    var node_id = $selected.attr('data-id') || null;
//                    this.redraw(node_id);
//                },
//                post_filtered   : function (ids) {
//                    this.publish('filter_count', ids ? ids.length : null)
//                        ._prepareScrolledSize();
//
//                    var search_term = uijet.Resource('NodesListState').get('search');
//                    uijet.utils.requestAnimFrame( this.toggleHighlight.bind(this, search_term) );
//                    uijet.utils.requestAnimFrame( this.scroll.bind(this) );
//                }
//            },
//            app_events      : {
//                'legends_list.last_deleted'                 : 'sleep',
//                'search.changed'                            : 'updateSearchFilter+',
//                'selected.changed'                          : 'updateSelectedFilter+',
//                'nodes_list.filtered'                       : 'filterChildren',
//                'nodes_breadcrumbs.selected'                : 'redraw+',
//                'nodes_list_header.selected'                : 'sortNodes+',
//                'nodes_list.selection'                      : function () {
//                    var resource = this.resource;
                    //update DOM with collection's state
//                    this.$children.each(function (i, node) {
//                        var $node = uijet.$(node),
//                            id = $node.attr('data-id'),
//                            state = resource.get(id).get('selected');
//                        $node.attr('data-selected', state);
//                    });
//                    if ( this.active_filters & this.filter_flags['selected'] ) {
//                        this.updateSelectedFilter(true);
//                    }
//                }
//            }
//        }
    }];

});
