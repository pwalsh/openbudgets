define([
    'uijet_dir/uijet',
    'resources'
], function (uijet, resources) {

    var arraySort = Array.prototype.sort;

    uijet.Adapter('NodesList', {
        redraw          : function (scope) {
            var filter = this.search_active ?
                    this.resource.byAncestor :
                    this.resource.byParent; 
            this.scope_changed = true;
            this.scope = scope || null;
            this.filter(filter, this.scope)
                .render();
        },
        sortItems       : function (data) {
            this.desc = data.desc;
            this.sort((data.desc ? '-' : '') + data.column);
            if ( this.filtered && ! uijet.Utils.isFunc(this.filtered) ) {
                this.filtered = arraySort.call(this.filtered, resources.utils.reverseSorting(data.column));
                if ( ! data.desc ) {
                    this.filtered.reverse();
                }
            }
            this.render();
        },
        searchFilter    : function (query) {
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
        buildIndex      : function () {
            this.index()
                .search_index.add(
                    this.resource.byAncestor(this.scope)
                        .map(uijet.Utils.prop('attributes'))
                );
        },
        updateSelection : function (id) {
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
                    // selecting
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
        }
    });

});
