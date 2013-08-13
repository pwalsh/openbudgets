define([
    'uijet_dir/uijet',
    'resources',
    'controllers/ItemsList',
    'ui/sheet'
], function (uijet, resources) {

    uijet.Resource('ItemsSearchResult', resources.Items);

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

                    this.scope = window.ITEM.node || null;
                    this.resource.reset(this.resource.parse(window.ITEMS_LIST));
                    this.index();

                    this.options.fetch_options.data.sheets = state_model.get('sheet');
                    
                    this.listenTo(state_model, 'change:sheet', function (model, value) {
                        var prev = model.previous('sheet'), prev_sheets, prev_sheet;

                        // make sure we cache the previous sheet
                        if ( prev ) {
                            prev_sheets = uijet.Resource('PreviousSheets');

                            // assigning in purpose to reuse as previous sheet
                            if ( prev_sheet = prev_sheets.get(prev) ) {
                                // update cache of previous Items collection with current LatestSheet state
                                prev_sheet.get('items').set(this.resource.models, { remove : false });
                            }
                            else {
                                prev_sheets.add({
                                    id      : prev,
                                    items   : this.resource.clone()
                                });
                            }
                        }

                        this.wake({
                            sheets  : value,
                            scope   : model.hasChanged('scope') ? model.get('scope') : null
                        });
                    })
                    .listenTo(state_model, 'change:scope', function (model, scope) {
                        if ( ! model.hasChanged('sheet') ) {
                            this.wake({
                                scope   : scope || null
                            });
                        }
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
                        undef = void 0,
                        scope = 'scope' in this.context ? this.context.scope || null : undef,
                        sheet = this.context.sheets,
                        search = this.context.search || state.get('search'),
                        prev_sheet;

                    if ( sheet && (prev_sheet = uijet.Resource('PreviousSheets').get(sheet)) ) {
                        this.resource = prev_sheet.get('items');
                        // register current collection as the new instance
                        uijet.Resource('LatestSheet', this.resource, true);
                        scope = scope === -1 ?
                            this.resource.findWhere({ uuid : state.get('uuid') }).get('node') :
                            scope;
                    }
                    // if for some reason scope is still unknown reset it to `null`
                    if ( scope === -1 ) {
                        scope = null;
                    }

                    this.search_active = !!search;

                    delete this.filtered;
                    this.has_data = false;

                    if ( sheet ) {
                        this.sheet_changed = true;
                        if ( ! prev_sheet ) {
                            // reuse this collection
                            this.options.fetch_options.reset = true;
                        }
                        this.options.fetch_options.data.sheets = sheet;
                    }

                    if ( search ) {
                        this.options.fetch_options.data.search = search;
                        delete this.options.fetch_options.data.parents;
                    }
                    else {
                        delete this.options.fetch_options.data.search;
                        this.options.fetch_options.data.parents = (scope === undef ? this.scope : scope) || 'none';
                    }

                    // set scope if it's defined in the context
                    scope !== undef && this.setScope(scope);
                },
                pre_update      : 'spin',
                post_fetch_data : function (response) {
                    var scope_changed = this.scope_changed;
                    // after we had to reset because of sheet change make sure turn reset off again
                    if ( this.options.fetch_options.reset ) {
                        this.options.fetch_options.reset = false;
                    }
                    if ( this.search_active ) {
                        this.filter(uijet.Resource('ItemsSearchResult')
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
                    if ( this.sheet_changed ) {
                        this.sheet_changed = false;
                        scope_changed || this.publish('sheet_changed', null);
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
                    
                    uijet.Resource('ItemsListState').set('scope', node_id);
                }
            },
            app_events      : {
                'items_breadcrumbs.selected'                : 'post_select+',
                'items_breadcrumbs_history_menu.selected'   : 'post_select+',
                'items_list_header.selected'                : 'sortItems+'
            }
        }
    }];

});
