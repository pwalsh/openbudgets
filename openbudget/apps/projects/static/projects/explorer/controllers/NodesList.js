define([
    'uijet_dir/uijet',
    'resources'
], function (uijet, resources) {

    var arraySort = Array.prototype.sort;

    uijet.Adapter('NodesList', {
        redraw              : function (scope) {
            var filter = this.active_filters ?
                    this.resource.byAncestor :
                    this.resource.byParent; 
            this.scope_changed = true;
            this.scope = scope || null;
            return this.filter(filter, this.scope)
                       .render();
        },
        buildIndex          : function () {
            this.index()
                .search_index.add(
                    this.resource.byAncestor(this.scope)
                        .map(uijet.utils.prop('attributes'))
                );
            return this;
        },
        sortNodes           : function (data) {
            this.desc = data.desc;
            this.sort((data.desc ? '-' : '') + data.column);
            if ( this.filtered && ! uijet.utils.isFunc(this.filtered) ) {
                this.filtered = arraySort.call(this.filtered, resources.utils.reverseSorting(data.column));
                if ( ! data.desc ) {
                    this.filtered.reverse();
                }
            }
            return this.render();
        },
        updateSearchFilter  : function (data) {
            var query = data.args[1];
            if ( query === null ) {
                this.search_active = false;
                this.active_filters--;

                if ( ! this.active_filters ) {
                    this.filter(this.resource.byParent, this.scope)
                        .render();
                }
            }
            else {
                if ( ! this.search_active ) {
                    this.search_active = true;
                    this.active_filters++;

                    if ( this.active_filters === 1 ) {
                        this.filter(this.resource.byAncestor, this.scope)
                            .render();
                    }
                }
            }
            this.filterBySearch(query);
            return this;
        },
        updateSelectedFilter: function (data) {
            var state = data.args[1];
            if ( state === null ) {
                this.selected_active = false;
                this.active_filters--;

                if ( ! this.active_filters ) {
                    this.filter(this.resource.byParent, this.scope)
                        .render();
                }
            }
            else if ( state ) {
                this.selected_active = true;
                this.active_filters++;
            }
            this.filterBySelected(state);
            return this;
        },
        resetSelection      : function (state) {
            var selected_state = { selected : 'selected' },
                partial_state = { selected : 'partial' },
                unselected_state = { selected : '' },
                len = this.resource.length,
                model, selected, partial;

            state = state || {};
            selected = state.selected;
            partial = state.partial;

            while ( len-- ) {
                model = this.resource.models[len];
                model.set(unselected_state);
            }

            len = selected && selected.length;
            while ( len-- ) {
                this.resource.get(selected[len]).set(selected_state);
            }

            len = partial && partial.length;
            while ( len-- ) {
                this.resource.get(partial[len]).set(partial_state);
            }

            return this;
        },
        updateSelection     : function (id) {
            var model = this.resource.get(id),
                old_state = model.get('selected'),
                new_state = { selected : '' },
                resource = this.resource,
                previous_id = id,
                branch, is_partial, target_selected;
            if ( old_state !== 'selected' ) {
                new_state.selected = 'selected';
            }

            /*
             * Update the clicked row's model
             */
            model.set(new_state);

            target_selected = new_state.selected === 'selected';

            /*
             * Update all descendants
             */
            //! Array.prototype.forEach
            this.resource.byAncestor(id).forEach(function (model) {
                model.set(new_state);
            });

            /*
             * Update all ancestors
             */
            branch = this.resource.branch(id);
            // remove this model from the branch
            branch.pop();
            //! Array.prototype.forEach
            branch.reverse().forEach(function (model) {
                if ( is_partial ) {
                    model.set(new_state);
                    return;
                }
                var old_branch_state = model.get('selected'),
                    children = model.get('children');
                switch ( old_branch_state ) {
                    case 'selected':
                        if ( children.length > 1 ) {
                            new_state.selected = 'partial';
                            is_partial = true;
                        }
                        model.set(new_state);
                        break;
                    case 'partial':
                        if ( children.length > 1 ) {
                            //! Array.prototype.some
                            is_partial = children.some(function (child_id) {
                                if ( child_id !== previous_id ) {
                                    var _state = resource.get(child_id).get('selected');
                                    return target_selected ?
                                        _state !== 'selected' :
                                        _state === 'selected';
                                }
                            });
                            if ( is_partial ) {
                                new_state.selected = 'partial';
                            }
                        }
                        model.set(new_state);
                        break;
                    default:
                        if ( children.length > 1 ) {
                            new_state.selected = 'partial';
                            is_partial = true;
                        }
                        model.set(new_state);
                }
                previous_id = model.id;
            });
            return this;
        }
    });

});
