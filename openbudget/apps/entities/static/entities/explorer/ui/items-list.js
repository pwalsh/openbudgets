define([
    'uijet_dir/uijet',
    'resources',
    'project_widgets/FilteredList',
    'controllers/ItemsList'
], function (uijet, resources) {

    return [{
        type    : 'List',
        config  : {
            element     : '#items_list_header',
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
        type    : 'FilteredList',
        config  : {
            element         : '#items_list',
            mixins          : ['Templated', 'Scrolled'],
            adapters        : ['jqWheelScroll', 'Spin', 'ItemsList'],
            resource        : 'LatestSheet',
            position        : 'fluid',
            fetch_options   : {
                reset   : true,
                cache   : true,
                expires : 8 * 3600
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
                code        : 'code',
                '-code'     : resources.utils.reverseSorting('code'),
                direction   : 'direction',
                '-direction': resources.utils.reverseSorting('direction'),
                budget      : 'budget',
                '-budget'   : resources.utils.reverseSorting('budget'),
                actual      : 'actual',
                '-actual'   : resources.utils.reverseSorting('actual')
            },
            data_events     : {},
            signals         : {
                pre_wake        : function () {
                    // usually on first load when there's no context, just bail out
                    if ( ! this.context ) return false;

                    // change view back to main
                    this.setScope(null);

                    var state = uijet.Resource('ItemsListState');
                    this.updateFlags(state.attributes);

                    if ( this.active_filters ) {
                        this.filter(this.resource.byAncestor)
                    }
                    else {
                        this.filter(this.resource.roots);
                    }
                },
                pre_update      : 'spin',
                post_fetch_data : function () {
                    if ( this.queued_filters ) {
                        this.queued_filters = false;
                        this.filter(this.resource.byAncestor);
                    }
                    if ( this.reselect ) {
                        this.reselect = false;
                        this.resetSelection(this.context.selection);
                    }
                    if ( this.rebuild_index ) {
                        // clear FilterList's cache
                        this.rebuild_index = false;
                        this.cached_results = {};
                        this.$last_filter_result = null;
                        // rebuild index
                        this.buildIndex();
                    }
                    this.spinOff();
                },
                post_render     : function () {
                    this.$children = this.$element.children();
                    if ( this.active_filters ) {
                        this.filterChildren();
                    }
                    else {
                        this.scroll();
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
                },
                post_filtered   : function (ids) {
                    this.publish('filter_count', ids ? ids.length : null)
                        ._prepareScrolledSize();

                    var search_term = uijet.Resource('NodesListState').get('search');
                    uijet.utils.requestAnimFrame( this.toggleHighlight.bind(this, search_term) );
                    uijet.utils.requestAnimFrame( this.scroll.bind(this) );
                }
            },
            app_events      : {
                'search.changed'                            : 'updateSearchFilter+',
                'selected.changed'                          : 'updateSelectedFilter+',
                'items_list.filtered'                       : 'filterChildren',
                'item_breadcrumb_main.clicked'              : function () {
                    this.redraw(null);
                },
                'item_breadcrumb_back.clicked'              : function (data) {
                    this.redraw(data.context.id);
                },
                'items_breadcrumbs.selected'                : 'post_select+',
                'items_breadcrumbs_history_menu.selected'   : 'post_select+',
                'items_list_header.selected'                : 'sortItems+',
                'items_list.selection'                      : function () {
                    var resource = this.resource;
                    // update DOM with collection's state
                    this.$children.each(function (i, item) {
                        var $item = uijet.$(item),
                            id = +$item.attr('data-id'),
                            state = resource.get(id).get('selected');
                        $item.attr('data-selected', state);
                    });
                    if ( this.active_filters & this.filter_flags['selected'] ) {
                        this.updateSelectedFilter(true);
                    }
                }
            }
        }
    }];

});
