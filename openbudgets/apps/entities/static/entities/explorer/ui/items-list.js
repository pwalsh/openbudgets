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
                code        : resources.utils.nestingSort,
                '-code'     : resources.utils.reverseNestingSort,
                direction   : 'direction',
                '-direction': resources.utils.reverseSorting('direction'),
                budget      : 'budget',
                '-budget'   : resources.utils.reverseSorting('budget'),
                actual      : 'actual',
                '-actual'   : resources.utils.reverseSorting('actual')
            },
            data_events     : {
                request : function (resource, xhr, options) {
                    if ( this.last_request && this.last_request.state() == 'pending' ) {
                        this.last_request.abort();
                    }
                    this.last_request = xhr;
                },
                reset   : function () {
                    this.has_data = true;
                    delete this.$original_children;
                },
                sort    : function () {
                    uijet.Resource('ItemsListState').set('comments_item', null);
                }
            },
            signals         : {
                post_init       : function () {
                    var state_model = uijet.Resource('ItemsListState');

                    this.scope = window.ITEM.node || null;
                    this.resource.reset(this.resource.parse(window.ITEMS_LIST));
                    this.index();

                    this.options.fetch_options.data.sheets = state_model.get('sheet');
                    
                    this.listenTo(state_model, 'change', function (model, options) {
                        var changed = model.changedAttributes(),
                            search = null,
                            sheet, scope,
                            prev, prev_sheets, prev_sheet;

                        if ( ! changed )
                            return;

                        if ( 'search' in changed ) {
                            search = model.get('search');
                            if ( ! search ) {
                                prev = state_model.previous('search');
                                if ( ! prev ) {
                                    state_model.set('search', null, { silent : true });
                                    return;
                                }
                            }
                        }

                        if ( 'sheet' in changed ) {
                            prev = model.previous('sheet');

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
                            sheet = model.get('sheet');
                        }
                        else if ( 'scope' in changed ) {
                            scope = model.get('scope');
                        }
                        else if ( ! ('search' in changed) ) {
                            // move along people, nothing to see here
                            return;
                        }

                        this._finally().wake({
                            sheets  : sheet,
                            search  : search,
                            scope   : scope === void 0 ? model.get('scope') : scope || null
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

                    if ( sheet ) {
                        if ( prev_sheet = uijet.Resource('PreviousSheets').get(sheet) ) {
                            this.resource = prev_sheet.get('items');
                            // register current collection as the new instance
                            uijet.Resource('LatestSheet', this.resource, true);
                            scope = scope === -1 ?
                                this.resource.findWhere({ id : state.get('id') }).get('node') :
                                scope;
                        }
                        else {
                            // instantiate a new collection
                            this.resource = new resources.Items();
                            // register it
                            uijet.Resource('LatestSheet', this.resource, true);
                        }
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
                    var is_comment_button = uijet.$(e.target).hasClass('item_comment_button');

                    if ( is_comment_button ) {
                        uijet.Resource('ItemsListState').set('comments_item', $selected);
                        return false;
                    }
                    else {
                        return $selected.attr('data-id');
                    }
                },
                post_select     : function ($selected) {
                    var node_id = (typeof $selected == 'string' ?
                            $selected :
                            $selected.attr('data-id')) || null;
                    
                    uijet.Resource('ItemsListState').set('scope', node_id);
                }
            },
            app_events      : {
                'items_breadcrumbs.selected'                : 'post_select+',
                'items_list_header.selected'                : 'sortItems+',
                'comment_created'                           : function (response) {
                    var item = this.resource.get(response.item),
                        discussion,
                        sheet_re;
                    if ( item ) {
                        discussion = item.get('discussion') || [];
                        discussion.push(response);
                        item.set('discussion', discussion);

                        // we create a regex to test against keys that contain current sheet in cache
                        sheet_re = RegExp('sheets=' + this.options.fetch_options.data.sheets);

                        // clear all cache related to this sheet - just in case
                        Object.keys(resources.Backbone.fetchCache._cache).forEach(function (key) {
                            if ( sheet_re.test(key) ) {
                                resources.Backbone.fetchCache.clearItem(key);
                            }
                        }, this);

                        // bump the number of comments on the item
                        this.$element
                            .find('[data-item=' + response.item + ']')
                            .find('.item_comment_button')
                                .text(discussion.length);
                    }
                }
            }
        }
    }];

});
