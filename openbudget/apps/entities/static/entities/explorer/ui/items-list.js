define([
    'uijet_dir/uijet',
    'resources',
    'project_widgets/FilteredList',
    'controllers/ItemsList',
    'ui/sheet'
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
                remove  : false,
                cache   : true,
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
                search  : 'search'
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
            data_events     : {
                reset   : function () {
                    this.has_data = true;
                    delete this.$original_children;
                }
            },
            signals         : {
                post_init       : function () {
                    var state_model = uijet.Resource('ItemsListState');

                    this.resource.reset(this.resource.parse(window.ITEMS_LIST));

                    this.options.fetch_options.data.sheets = state_model.get('sheet');
                    
                    this.listenTo(state_model, 'change:sheet', function (model, value) {
                        this.options.fetch_options.reset = true;
                        this.wake({
                            sheets  : value,
                            scope   : null
                        });
                    }.bind(this));
                },
                pre_wake        : function () {
                    // usually on first load when there's no context, just bail out
                    if ( ! this.context ) return false;

                    var state = uijet.Resource('ItemsListState'),
                        scope = this.context.scope || null,
                        sheet = this.context.sheets;
                    this.updateFlags(state.attributes);

                    if ( this.all_fetched ) {
                        if ( this.active_filters ) {
                            this.filter(this.resource.byAncestor)
                        }
                        else {
                            this.filter(this.resource.roots);
                        }
                    }
                    else {
                        delete this.filtered;
                        this.has_data = false;
                        this.options.fetch_options.data.parents = scope || 'none';
                        if ( sheet ) {
                            this.options.fetch_options.data.sheets = sheet;
                        }
                    }
                    // change view back to main
                    this.setScope(scope);
                },
                pre_update      : 'spin',
                post_fetch_data : function () {
                    // after we had to reset because of sheet change make sure turn reset off again
                    if ( this.options.fetch_options.reset ) {
                        this.options.fetch_options.reset = false;
                    }
                    if ( this.queued_filters ) {
                        this.queued_filters = false;
                        this.filter(this.resource.byAncestor);
                    }
                    else {
                        this.filter(this.resource.byParent, this.scope);
                    }

                    if ( this.scope_changed ) {
                        this.scope_changed = false;
                        this._publishScope();
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
                    return id;
                },
                post_select     : function ($selected) {
                    var node_id = typeof $selected == 'number' ?
                        $selected :
                        +$selected.attr('data-id') || null;
                    this.all_fetched ?
                        this.redraw(node_id) :
                        this.wake({ scope : node_id });
                },
                post_filtered   : function (ids) {
                    this.publish('filter_count', ids ? ids.length : null)
                        ._prepareScrolledSize();

                    var search_term = uijet.Resource('ItemsListState').get('search');
                    uijet.utils.requestAnimFrame( this.toggleHighlight.bind(this, search_term) );
                    uijet.utils.requestAnimFrame( this.scroll.bind(this) );
                }
            },
            app_events      : {
                'search.changed'                            : 'updateSearchFilter+',
                'items_list.filtered'                       : 'filterChildren',
                'item_breadcrumb_main.clicked'              : function () {
                    this.redraw(null);
                },
                'item_breadcrumb_back.clicked'              : function (data) {
                    this.redraw(data.context.id);
                },
                'items_breadcrumbs.selected'                : 'post_select+',
                'items_breadcrumbs_history_menu.selected'   : 'post_select+',
                'items_list_header.selected'                : 'sortItems+'
            }
        }
    }];

});
