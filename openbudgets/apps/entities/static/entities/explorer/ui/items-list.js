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
                    page_by         : 4000,
                    node_parents    : 'none',
                    with_ancestors  : 'true'
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
                request             : function (resource, xhr, options) {
                    if ( this.last_request && this.last_request.state() == 'pending' ) {
                        this.last_request.abort();
                    }
                    else {
                        this.spin();
                    }
                    this.last_request = xhr;
                },
                sync                : function (resource, response) {
                    var scope_changed = this.scope_changed,
                        search_result;

//                    this.index();

                    // after we had to reset because of sheet change make sure we turn reset off again
                    if ( this.options.fetch_options.reset ) {
                        this.options.fetch_options.reset = false;
                    }

                    if ( this.search_active ) {
                        search_result = uijet.Resource('ItemsSearchResult');
                        search_result.reset(response.results);
                        this.setContext({
                            filtered: search_result.byAncestor(this.scope),
                            filter  : null
                        });
                    }
                    else {
                        this.setContext({
                            filter      : 'byParent',
                            filter_args : [this.scope] 
                        });
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
                error               : 'spinOff',
                reset               : function () {
                    delete this.$original_children;
                },
                sort                : function () {
                    uijet.Resource('ItemsListState').set('comments_item', null);
                }//,
//                'update:comments'   : function (model) {
                    // bump the number of comments on the item
//                    var $button  = this.$element.find('[data-item=' + model.get('id') + ']');

                    // if it's an item from the list and not scope item
//                    if ( $button.length ) {
                        // set the buttons
//                        $button.find('.item_comment_button')
//                            .text(model.get('comment_count'));
//                    }
//                    else {
                        // it's the scope item so notify the sheet_scope_comments
//                        uijet.publish('scope_comment_created', model);
//                    }
//                }
            },
            signals         : {
                post_init       : function () {
                    var state_model = uijet.Resource('ItemsListState');

                    this.scope = window.ITEM.node || null;
                    // set the initial filtering scope
                    if ( this.scope ) {
                        this.setContext({
                            filter      : 'byParent',
                            filter_args : [this.scope] 
                        });
                    }

                    this.resource.reset(this.resource.parse(window.ITEMS_LIST));
                    if (window.ITEM.id) {
                        this.resource.add(window.ITEM);
                    }
                    // needed for highlighting search terms in results
                    this.index();

                    this.options.fetch_options.data.sheets = state_model.get('sheet');
                    
                    this.listenTo(state_model, 'change', function (model, options) {
                        var changed = model.changedAttributes(),
                            fetch_ops_data = this.options.fetch_options.data,
                            search = model.get('search') || null,
                            sheet, scope,
                            prev, prev_sheets, prev_sheet, cached_sheet;

                        if ( ! changed )
                            return;

                        if ( 'search' in changed ) {
                            if ( ! search ) {
                                prev = state_model.previous('search');
                                if ( ! prev ) {
                                    // clean search to be `null` instead of empty string
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

                        // reset scope
                        scope = scope === void 0 ?
                                model.get('scope') :
                                scope || null;

                        if ( sheet ) {
                            if ( cached_sheet = prev_sheets.get(sheet) ) {
                                this.setResource(cached_sheet.get('items'));
                                scope = scope === -1 ?
                                    this.resource.findWhere({ node : state_model.get('node') }).get('node') :
                                    scope;
                            }
                            else {
                                this.setResource(new resources.Items());
                            }
                        }

                        // if for some reason scope is still unknown reset it to `null`
                        if ( scope === -1 ) {
                            scope = null;
                        }

                        this.search_active = !!search;

                        // ensure cleaning of last search results
                        delete this.getContext().filtered;

                        if ( sheet ) {
                            this.sheet_changed = true;
                            fetch_ops_data.sheets = sheet;
                        }

                        if ( search ) {
                            fetch_ops_data.search = search;
                            delete fetch_ops_data.node_parents;
                        }
                        else {
                            delete fetch_ops_data.search;
                            fetch_ops_data.node_parents = (typeof scope == 'undefined' ? this.scope : scope) || 'none';
                        }

                        this.setScope(scope);

                        this._finally()
                            .resource.fetch(this.options.fetch_options)
                            .then(this.wake.bind(this, {scope: scope}));
                    });
                },
                pre_wake        : function () {
                    // usually on first load context is empty, just bail out
                    if ( ! ('scope' in this.getContext()) ) {
                        return false;
                    }
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
                'items_breadcrumbs.selected': 'post_select+',
                'items_list_header.selected': 'sortItems+',
                'comment_created'           : function (response) {
                    var item = this.resource.get(response.item),
                        sheet_re;
                    if ( item ) {
                        item.addComment(response);

                        // we create a regex to test against keys that contain current sheet in cache
                        sheet_re = RegExp('sheets=' + this.options.fetch_options.data.sheets);

                        // clear all cache related to this sheet - just in case
                        Object.keys(resources.Backbone.fetchCache._cache).forEach(function (key) {
                            if ( sheet_re.test(key) ) {
                                resources.Backbone.fetchCache.clearItem(key);
                            }
                        }, this);
                    }
                }
            }
        }
    }];

});
