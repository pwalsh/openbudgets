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

    uijet.Adapter('ItemsList', {
        // optimization hack to not call `this._prepareScrolledSize()` after `render()`
        scrolled            : false,
        _publishScope       : function () {
            var item_model;
            uijet.Resource('ItemsListState').set('scope', this.scope);

            item_model = this.scope ?
                this.resource.findWhere({ node : this.scope }) ||
                uijet.Resource('Breadcrumbs').findWhere({ node : this.scope }) ||
                uijet.Resource('InitialItem') :
                this.scope;

            return this.publish('scope_changed', item_model);
        },
        setScope            : function (scope) {
            scope = scope || null;
            if ( scope !== this.scope ) {
                this.scope = scope;
                if ( this.has_data ) {
                    this._publishScope();
                }
                else {
                    this.scope_changed = true;
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
        sortItems           : function (data) {
            this.desc = data.desc;
            this.sort((data.desc ? '-' : '') + data.column);

            if ( this.has_data ) {
                if ( ! this.filtered ) {
                    this.filtered = this.resource.models;
                }
                if ( this.filtered && ! uijet.utils.isFunc(this.filtered) ) {
                    this.filtered = arraySort.call(this.filtered, resources.utils.reverseSorting(data.column));
                    if ( ! data.desc ) {
                        this.filtered.reverse();
                    }
                }
                return this.render();
            }
            return this;
        },
        toggleHighlight     : function (search_term) {
            var resource = this.resource,
                highlight = this.highlight.bind(this),
                scope = this.scope,
                $list = this.$last_filter_result || this.$children,
                initial_item_height = $list.first().height();

            $list.each(function (i, item) {
                var model = resource.get(+item.getAttribute('data-item')),
                    name_text = model.get('name'),
                    code_text = model.get('code'),
                    $item = uijet.$(item),
                    name = $item.find('.item_cell_name')[0],
                    code = $item.find('.item_cell_code')[0],
                    optimize = i < max_results_limit_for_branch_name_optimization,
                    branch;

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
            });
        }
    });

});
