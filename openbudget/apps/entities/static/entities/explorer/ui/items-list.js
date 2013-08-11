define([
    'uijet_dir/uijet',
    'resources',
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
        type    : 'List',
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
                    this.index();

                    this.options.fetch_options.data.sheets = state_model.get('sheet');
                    
                    this.listenTo(state_model, 'change:sheet', function (model, value) {
                        this.options.fetch_options.reset = true;
                        this.wake({
                            sheets  : value,
                            scope   : null
                        });
                    })
                    .listenTo(state_model, 'change:scope', function (model, scope) {
                        this.wake({
                            scope   : scope || null
                        });
                    })
                    .listenTo(state_model, 'change:search', function (model, term) {
                        var prev;
                        if ( ! term ) {
                            prev = state_model.previous('search');
                            if ( ! prev ) {
                                state_model.set('search', null, { silent : true });
                                return;
                            }
                        }
                        this.wake({
                            search  : term
                        });
                    });
                },
                pre_wake        : function () {
                    // usually on first load when there's no context, just bail out
                    if ( ! this.context ) return false;

                    var state = uijet.Resource('ItemsListState'),
                        scope = this.context.scope || null,
                        sheet = this.context.sheets,
                        search = this.context.search;

                    this.search_active = !!search;

                    delete this.filtered;
                    this.has_data = false;
                    if ( sheet ) {
                        this.options.fetch_options.data.sheets = sheet;
                    }
                    if ( search ) {
                        this.options.fetch_options.data.search = search;
                        delete this.options.fetch_options.data.parents;
                    }
                    else {
                        this.options.fetch_options.data.parents = scope || 'none';
                    }
                    // change view back to main
                    this.setScope(scope);
                },
                pre_update      : 'spin',
                post_fetch_data : function (response) {
                    // after we had to reset because of sheet change make sure turn reset off again
                    if ( this.options.fetch_options.reset ) {
                        this.options.fetch_options.reset = false;
                    }
                    if ( this.search_active ) {
                        var search_result = [];
                        response.results.forEach(function (item) {
                            search_result.push(this.resource.get(item.id));
                        }, this);
                        this.filter(search_result);
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
                    if ( this.search_active ) {
                        var search_term = uijet.Resource('ItemsListState').get('search');

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
                pre_select      : function ($selected, e) {
                    return +$selected.attr('data-id');
                },
                post_select     : function ($selected) {
                    var node_id = typeof $selected == 'number' ?
                        $selected :
                        +$selected.attr('data-id') || null;
                    
                    this.wake({ scope : node_id });
                }
            },
            app_events      : {
                'search.changed'                            : function () {
                    console.log(arguments);
                },
                'items_breadcrumbs.selected'                : 'post_select+',
                'items_breadcrumbs_history_menu.selected'   : 'post_select+',
                'items_list_header.selected'                : 'sortItems+'
            }
        }
    }];

});
