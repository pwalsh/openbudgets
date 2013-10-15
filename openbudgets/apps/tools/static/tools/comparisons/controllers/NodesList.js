define([
    'uijet_dir/uijet',
    'resources'
], function (uijet, resources) {

    var arraySort = Array.prototype.sort,
        spanWrap = function (strings) {
            return '<span>' + strings.join('</span><span>') + '</span>';
        },
        max_results_limit_for_branch_name_optimization = 100,
        fixBranchText = function (name, branch, initial_item_height) {
//            uijet.utils.requestAnimFrame(function () {
            var first_try = true,
                middle_index;
            while ( name.offsetHeight > initial_item_height ) {
                middle_index = Math.floor((branch.length - 1) / 2);
                if ( first_try ) {
                    first_try = false;
                    branch[middle_index] = '...';
                }
                else {
                    branch.splice(middle_index, 1);
                }
                name.innerHTML = spanWrap(branch);
            }
//            });
        };

    uijet.Adapter('NodesList', {
        // optimization hack to not call `this._prepareScrolledSize()` after `render()`
        scrolled            : false,
        setScope            : function (scope) {
            scope = scope || null;
            if ( scope !== this.scope ) {
                this.scope = scope;
                if ( this.has_data ) {
                    this.publish('scope_changed', this.scope && this.resource.get(this.scope));
                    this.buildIndex();
                }
                else {
                    this.rebuild_index = true;
                }
            }
            return this;
        },
        redraw              : function (scope) {
            var filter = this.active_filters ?
                    this.resource.byAncestor :
                    this.resource.byParent; 
            this.setScope(scope);
            return this.filter(filter, this.scope)
                       .render();
        },
        buildIndex          : function () {
            this.cached_results = {};
            this.index()
                .search_index.add(
                    this.resource.byAncestor(this.scope)
                        .map(uijet.utils.prop('attributes'))
                );
            if ( this.active_filters ) {
                // refill cache
                this.filterItems();
            }
            return this;
        },
        sortNodes           : function (data) {
            var sorting_key = (data.desc ? '-' : '') + data.column,
                is_comparator_function = uijet.utils.isFunc(this.options.sorting[sorting_key]);
            this.desc = data.desc;
            this.sort(sorting_key);

            if ( this.has_data ) {
                if ( this.filtered && ! uijet.utils.isFunc(this.filtered) ) {
                    this.filtered = arraySort.call(
                        this.filtered,
                        is_comparator_function ?
                            this.options.sorting[sorting_key] :
                            resources.utils.reverseSorting(data.column)
                    );

                    if ( ! is_comparator_function && ! data.desc ) {
                        this.filtered.reverse();
                    }
                }
                return this.render();
            }
            return this;
        },
        updateSearchFilter  : function (data) {
            var query = uijet.utils.isObj(data) ? data.args[1] : data,
                filters_active = !!this.active_filters;

            if ( query === void 0 ) {
                return this.clearFilter('search');
            }

            this.filterBySearch(query);

            return this._updateFilter(!!this.active_filters !== filters_active);
        },
        updateSelectedFilter: function (data) {
            var state = uijet.utils.isObj(data) ? data.args[1] : data,
                filters_active = !!this.active_filters;

            if ( state === void 0 ) {
                return this.clearFilter('selected');
            }

            this.filterBySelected(state);

            return this._updateFilter(!!this.active_filters !== filters_active);
        },
        _updateFilter       : function (redraw) {
            if ( this.has_data && this.$children ) {
                if ( redraw ) {
                    this.redraw(this.scope);
                }
                else {
                    this.publish('filtered');
                }
            }
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
        },
        toggleHighlight     : function (search_term) {
            var resource = this.resource,
                highlight = this.highlight.bind(this),
                scope = this.scope,
                $list = this.$last_filter_result || this.$children,
                initial_item_height = $list.first().height();
            $list.each(function (i, item) {
                var model = resource.get(item.getAttribute('data-id')),
                    name_text = model.get('name'),
                    code_text = model.get('code'),
                    $item = uijet.$(item),
                    name = $item.find('.node_cell_name')[0],
                    code = $item.find('.node_cell_code')[0],
                    optimize = i < max_results_limit_for_branch_name_optimization,
                    branch;
                if ( search_term ) {
                    branch = model.branchName(scope);
                    if ( ! optimize && branch.length > 1 ) {
                        branch.length = 1;
                        branch.push('...');
                    }
                    branch.push(highlight(name_text, search_term));
                    name.innerHTML = spanWrap(branch);
                    code.innerHTML = highlight(code_text, search_term);
                    if ( optimize && name.offsetHeight > initial_item_height ) {
                        fixBranchText(name, branch, initial_item_height);
                    }
                }
                else {
                    name.innerHTML = '';
                    code.innerHTML = '';
                    name.appendChild(document.createTextNode(name_text));
                    code.appendChild(document.createTextNode(code_text));
                }
            });
        }
    });

});
