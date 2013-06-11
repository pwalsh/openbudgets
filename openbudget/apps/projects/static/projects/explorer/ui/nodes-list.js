define([
    'uijet_dir/uijet',
    'resources',
    'controllers/SearchedList'
], function (uijet, resources) {

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element     : '#nodes_list_container',
            dont_wake   : true,
            app_events  : {
                'entities_list.selected': function ($selected) {
                    this.wake({ entity_id : $selected.attr('data-id') });
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
        type    : 'List',
        config  : {
            element     : '#nodes_list',
            mixins      : ['Templated', 'Scrolled'],
            adapters    : ['jqWheelScroll', 'Spin', 'SearchedList'],
            resource    : 'LatestTemplate',
            position    : 'fluid',
            search      : {
                fields  : {
                    name        : 10,
                    description : 1,
                    code        : 20
                }
            },
            sorting     : {
                name        : 'name',
                '-name'     : resources.utils.reverseSorting('name'),
                code        : 'code',
                '-code'     : resources.utils.reverseSorting('code'),
                direction   : 'direction',
                '-direction': resources.utils.reverseSorting('direction')
            },
            signals     : {
                post_init       : function () {
                    this.scope = null;
                },
                pre_wake        : function () {
                    var entity_id = this.context.entity_id;
                    if ( entity_id ) {
                        if ( this.latest_entity_id !== entity_id ) {
                            this.latest_entity_id = entity_id;
                            // this makes sure search index is rebuilt and view is re-rendered
                            this.scope_changed = true;
                            // this makes sure the resource will execute fetch to sync with remote server
                            this.has_data = false;
                            this.scope = null;
                            this.resource.url = API_URL + 'nodes/latest/' + entity_id + '/';
                            this.filter(this.resource.roots);
                        }
                        else {
                            this.scope_changed = false;
                        }
                    }
                    return this.scope_changed;
                },
                pre_update      : 'spin',
                post_fetch_data : 'spinOff',
                pre_render      : function () {
                    this.has_content && this.$element.addClass('invisible');
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    var query = uijet.Resource('NodesListState').get('search');
                    if ( this.scope_changed ) {
                        this.scope_changed = false;
                        this.index()
                            .search_index.add(
                                this.resource.byAncestor(this.scope)
                                    .map(uijet.Utils.prop('attributes'))
                            );
                    }
                    if ( query ) {
                        this.filterItems(query);
                    }
                    else {
                        this.scroll()
                            .$element.removeClass('invisible');
                    }
                    this._finally();
                },
                pre_select      : function ($selected, e) {
                    //TODO: refactor me!!!
                    var id = +$selected.attr('data-id');
                    if ( uijet.$(e.target).hasClass('selectbox') ) {
                        var model = this.resource.get(id),
                            old_state = model.get('selected'),
                            new_state = { selected : '' },
                            resource = this.resource,
                            previous_id = id,
                            branch, is_partial;
                        switch ( old_state ) {
                            case 'selected':
                                // unselecting
                                model.set(new_state);
                                //! Array.prototype.forEach
                                this.resource.byAncestor(id).forEach(function (model) {
                                    model.set(new_state);
                                });
                                branch = this.resource.branch(id);
                                // remove this model from the branch
                                branch.pop();
                                //! Array.prototype.forEach
                                branch.reverse().forEach(function (model) {
                                    var old_branch_state = model.get('selected'),
                                        children = model.get('children'),
                                        new_branch_state = { selected : '' };
                                    if ( is_partial ) {
                                        model.set({ selected : 'partial' });
                                        return;
                                    }
                                    switch ( old_branch_state ) {
                                        case 'selected':
                                            if ( children.length > 1 ) {
                                                new_branch_state.selected = 'partial';
                                                is_partial = true;
                                            }
                                            model.set(new_branch_state);
                                            break;
                                        case 'partial':
                                            if ( children.length > 1 ) {
                                                //! Array.prototype.some
                                                is_partial = children.some(function (child_id) {
                                                    if ( child_id !== previous_id ) {
                                                        return resource.get(child_id).get('selected') === 'selected';
                                                    }
                                                });
                                                if ( is_partial ) {
                                                    new_branch_state.selected = 'partial';
                                                }
                                            }
                                            model.set(new_branch_state);
                                            break;
                                    }
                                    previous_id = model.id;
                                });
                                break;
                            case 'partial':
                            default:
                                new_state.selected = 'selected';
                                model.set(new_state);
                                //! Array.prototype.forEach
                                this.resource.byAncestor(id).forEach(function (model) {
                                    model.set(new_state);
                                });
                                branch = this.resource.branch(id);
                                // remove this model from the branch
                                branch.pop();
                                //! Array.prototype.forEach
                                branch.reverse().forEach(function (model) {
                                    var old_branch_state = model.get('selected'),
                                        children = model.get('children'),
                                        new_branch_state = { selected : 'selected' };
                                    if ( is_partial ) {
                                        model.set({ selected : 'partial' });
                                        return;
                                    }
                                    switch ( old_branch_state ) {
                                        case 'partial':
                                            if ( children.length > 1 ) {
                                                //! Array.prototype.some
                                                is_partial = children.some(function (child_id) {
                                                    if ( child_id !== previous_id ) {
                                                        return resource.get(child_id).get('selected') !== 'selected';
                                                    }
                                                });
                                                if ( is_partial ) {
                                                    new_branch_state.selected = 'partial';
                                                }
                                            }
                                            model.set(new_branch_state);
                                            break;
                                        default:
                                            if ( children.length > 1 ) {
                                                new_branch_state.selected = 'partial';
                                                is_partial = true;
                                            }
                                            model.set(new_branch_state);
                                            break;
                                    }
                                    previous_id = model.id;
                                });
                                break;
                        }
                        this.publish('selection');
                        return false;
                    }
                    else {
                        return ! $selected[0].hasAttribute('data-leaf') && id;
                    }
                },
                post_select     : function ($selected) {
                    var node_id = +$selected.attr('data-id') || null,
                        filter = this.search_active ?
                            this.resource.byAncestor :
                            this.resource.byParent;
                    // make sure we rebuild index and re-render
                    this.scope_changed = true;
                    this.scope = node_id || null;
                    this.filter(filter, node_id)
                        .render();
                }
            },
            app_events  : {
                'search.changed'                            : function (data) {
                    var query = data.args[1];
                    if ( query === null ) {
                        this.search_active = false;
                        this.filter(this.resource.byParent, this.scope)
                            .render();
                    } else {
                        if ( ! this.search_active ) {
                            this.search_active = true;
                            this.filter(this.resource.byAncestor, this.scope)
                                .render();
                        }
                        else {
                            this.filterItems(query);
                        }
                    }
                },
                'nodes_list.filtered'                       : function () {
                    this.scroll()
                        .$element.removeClass('invisible');
                },
                'node_breadcrumb_main.clicked'              : function () {
                    this.scope_changed = true;
                    this.scope = null;
                    this.filter(this.resource.roots)
                        .render();
                },
                'node_breadcrumb_back.clicked'              : function (data) {
                    var scope = data.context.id,
                        filter = this.search_active ?
                            this.resource.byAncestor :
                            this.resource.byParent; 
                    this.scope_changed = true;
                    this.scope = scope;
                    this.filter(filter, scope)
                        .render();
                },
                'nodes_breadcrumbs.selected'                : 'post_select+',
                'nodes_breadcrumbs_history_menu.selected'   : 'post_select+',
                'nodes_list_header.selected'                : function (data) {
                    this.desc = data.desc;
                    this.sort((data.desc ? '-' : '') + data.column);
                    if ( this.filtered && ! uijet.Utils.isFunc(this.filtered) ) {
                        this.filtered = Array.prototype.sort.call(this.filtered, resources.utils.reverseSorting(data.column));
                        if ( ! data.desc ) {
                            this.filtered.reverse();
                        }
                    }
                    this.render();
                },
                'nodes_list.selection'                      : function () {
                    var resource = this.resource,
                        filter = this.search_active ?
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
                }
            }
        }
    }]);

});
