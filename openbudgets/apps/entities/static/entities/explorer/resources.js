define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore',
    'api',
    'modules/promises/q',
    'backbone-fetch-cache'
], function (uijet, Backbone, _, api) {

    uijet.use({
        prop: function (property) {
            return function (obj) {
                return obj[property];
            };
        },
        formatCommas: function (obj) {
            return obj.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
    }, uijet.utils);

    var reverseSorting = function (field) {
            return function (a, b) {
                var a_val = a.get(field),
                    b_val = b.get(field);
                return a_val < b_val ?
                    1 :
                    a_val > b_val ?
                        -1 :
                        0;
            };
        },
        nestingSortFactory = function (reverse) {
            var a_is_smaller = reverse ? 1 : -1,
                a_is_bigger = reverse ? -1 : 1;
                
            return function (a, b) {
                var collection = a.collection,
                    a_attrs = a.attributes,
                    b_attrs = b.attributes,
                    a_ancestors = a_attrs.ancestors,
                    b_ancestors = b_attrs.ancestors,
                    n = 0, m = 0, 
                    a_top = a_attrs, b_top = b_attrs,
                    go_deeper = true,
                    a_code, b_code;
    
                do {
                    if ( a_ancestors[n] ) {
                        a_top = a_ancestors[n];
                        n += 1;
                    }
                    else {
                        go_deeper = false;
                        a_top = a_attrs;
                    }
                    if ( b_ancestors[m] ) {
                        b_top = b_ancestors[m];
                        m += 1;
                    }
                    else {
                        go_deeper = false;
                        b_top = b_attrs;
                    }
                }
                while ( go_deeper && a_top.id === b_top.id );
    
                a_code = a_top.code;
                b_code = b_top.code;
    
                // if `a` and `b` are not in same level
                return a_code == b_code ?
                    // check if `a` is higher in the hierarchy, otherwise `b` is
                    a_top === a_attrs ?
                        a_is_smaller : a_is_bigger :
                    // if they are in same level order by code
                    a_code < b_code ? a_is_smaller : a_is_bigger;
            };
        },
        /*
         * SheetItem Model
         */
        Item = uijet.Model({
            idAttribute : 'id',
            branchName  : function (from_id) {
                var ancestors = this.attributes.ancestors,
                    index = from_id ? 0 : null,
                    result = [],
                    ancestors_len = ancestors.length;

                if ( index !== null ) {
                    ancestors.some(function (ancestor) {
                        if ( ancestor.id === from_id ) {
                            return true
                        }
                        index++;
                        return false;
                    });
                    index += 1;
                }

                while ( ancestors_len > index ) {
                    ancestors_len -= 1;
                    result.unshift(ancestors[ancestors_len].name);
                }

                return result;
            },
            commas      : function () { 
                return function (text, render) {
                    return uijet.utils.formatCommas(render(text));
                };
            }
        }),
        /*
         * SheetItems Collection
         */
        Items = uijet.Collection({
            model           : Item,
            url             : function () {
                return api.getRoute('sheetItems');
            },
            comparator      : function (a, b) {
                var a_attrs = a.attributes,
                    b_attrs = b.attributes,
                    diff = a_attrs.level - b_attrs.level;
                if ( ! diff ) {
                    diff = a_attrs.code < b_attrs.code;
                    return diff ?
                        -1 :
                        a_attrs.code > b_attrs.code ?
                            1 :
                            0;
                }
                return diff > 0 ? 1 : -1;
            },
            /**
             * Setting `ancestors` array of `id`s, `leaf_item` boolean flag and
             * `level` - a Number representing the level of the item in the tree.
             * 
             * @param {Object|Array} response
             * @returns {Object|Array} response
             */
            parse           : function (response) {
                var results = response.results || response,
                    last = results.length - 1,
                    item, n;
                /* 
                 * first loop
                 *
                 * init `ancestor` to `[]`
                 * set `level` by splitting `path` and checking its `length`
                 * parse `actual` and `budget` to floats
                 * translate `direction`
                 * if no `children` or it's empty set `leaf_item` to `true`
                 */
                for ( n = last; item = results[n]; n-- ) {
                    item.ancestors || (item.ancestors = []);
                    item.level = item.path.split('|').length - 1;

                    // convert to integers
                    item.actual = item.actual | 0;
                    item.budget = item.budget | 0;

                    item.direction = gettext(item.direction);

                    if ( ! (item.children && item.children.length) ) {
                        item.leaf_item = true;
                    }
                }

                return results;
            },
            roots           : function () {
                return this.byParent(null);
            },
            byParent        : function (parent_id) {
                return this.filter(function (item) {
                    var parent = item.attributes.parent;
                    return (parent && parent.id) === parent_id;
                });
            },
            byAncestor      : function (ancestor_id) {
                if ( ancestor_id ) {
                    return this.filter(function (item) {
                        return item.attributes.ancestors.some(function (ancestor) {
                            return ancestor.id === ancestor_id
                        });
                    });
                }
                else {
                    return this.models;
                }
            },
            branch          : function (item_id) {
                var tip_item, branch;
                if ( item_id ) {
                    tip_item = this.get(item_id);
                    //! Array.prototype.map
                    branch = tip_item.get('ancestors')
                        .map( function (ancestor_id) {
                            return this.get(ancestor_id);
                        }, this );
                    branch.push(tip_item);
                }
                return branch || [];
            }
        }),
        Sheet = uijet.Model({
            idAttribute : 'id'
        }),
        /*
         * Collection of SheetItems collections
         */
        Sheets = uijet.Collection({
            model   : Sheet
        });

    return {
        Item    : Item,
        Items   : Items,
        Sheet   : Sheet,
        Sheets  : Sheets,
        utils   : {
            reverseSorting      : reverseSorting,
            nestingSort         : nestingSortFactory(false),
            reverseNestingSort  : nestingSortFactory(true)
        },
        '_'     : _,
        Backbone: Backbone
    };
});
