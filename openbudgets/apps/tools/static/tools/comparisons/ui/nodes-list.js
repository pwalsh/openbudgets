define([
    'uijet_dir/uijet',
    'resources',
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
                    this.spin();
                },
                reset   : function () {
                    delete this.$original_children;
                },
                sync    : function (response) {
                    var scope_changed = this.scope_changed,
                        search_result;
                    // after we had to reset because of entity change make sure turn reset off again
                    if ( this.options.fetch_options.reset ) {
                        this.options.fetch_options.reset = false;
                    }
                    if ( this.search_active ) {
                        search_result = uijet.Resource('NodesSearchResult');
                        search_result.reset(response.results);
                        this.setContext({
                            filtered: search_result.byAncestor(this.scope),
                            filter  : null
                        });
                    }
                    else {
                        this.setContext({
                            filter      : 'byParent',
                            filter_args : [this.scope] 
                        });
                    }

                    if ( scope_changed ) {
                        this.scope_changed = false;
                        this._publishScope();
                    }
                    if ( this.template_changed ) {
                        this.template_changed = false;
                        //TODO: check if we need to explicitly handle
//                        scope_changed || this.publish('sheet_changed', null);
                    }

                    this.spinOff();
                },
                error   : 'spinOff'
            },
            signals         : {
                post_init       : function () {
                    var state_model = uijet.Resource('NodesListState');

                    this.scope = null;
                    this.index();

                    this.listenTo(state_model, 'change', function (model, options) {
                        var changed = model.changedAttributes(),
                            fetch_ops_data = this.options.fetch_options.data,
                            search = model.get('search') || null,
                            entity_id, scope,
                            prev, prev_templates, prev_template, cached_template;

                        if ( ! changed )
                            return;

                        if ( 'search' in changed ) {
                            if ( ! search ) {
                                prev = state_model.previous('search');
                                if ( ! prev ) {
                                    // clean search to be `null` instead of empty string
                                    state_model.set('search', null, { silent : true });
                                    return;
                                }
                            }
                        }

                        if ( 'selection' in changed ) {
                            //TODO: this was copy-pasted from old nodes_list, need to check and fix
                            if ( 'scope' in this.getContext() ) {
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

                        if ( entity_id ) {
                            if ( cached_template = uijet.Resource('PreviousSheets').get(entity_id) ) {
                                // register current collection as the new instance
                                this.setResource(cached_template.get('nodes'));
                                scope = scope === -1 ?
                                    this.resource.findWhere(model.get('scope')).get('id') :
                                    scope;
                            }
                            else {
                                // instantiate a new collection and register it
                                this.setResource(new resources.Nodes());
                            }
                        }
                        // if for some reason scope is still unknown reset it to `null`
                        if ( scope === -1 ) {
                            scope = null;
                        }

                        this.search_active = !!search;

                        // ensure cleaning of last search results
                        delete this.getContext().filtered;

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
                            fetch_ops_data.parents = scope || 'none';
                        }

                        // set scope if it's defined in the context
                        this.setScope(scope);

                        this._finally()
                            .resource.fetch(this.options.fetch_options)
                            .then(this.wake.bind(this, {
                                entity_id   : entity_id,
                                search      : search,
                                scope       : scope === void 0 ? model.get('scope') : scope || null
                            }));
                    });
                },
                pre_wake        : function () {
                    // usually on first load, just bail out
                    if ( ! ('scope' in this.getContext() ) ) return false;
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
                'nodes_list_header.selected': 'sortNodes+',
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
    }];

});
