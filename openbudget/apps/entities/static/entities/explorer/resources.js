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
        nestingSort = function (a, b) {
            var a_attrs = a.attributes,
                b_attrs = b.attributes,
                a_parent = a_attrs.parent,
                b_parent = b_attrs.parent,
                collection, a_leaf, b_leaf;

            if ( a_parent === b_parent ) {
                a_leaf = a_attrs.leaf_item;
                b_leaf = b_attrs.leaf_item;
                if ( a_leaf && ! b_leaf )
                    return -1;
                else if ( b_leaf && ! a_leaf )
                    return 1;

                return a_attrs.code < b_attrs.code ? -1 : 1;
            }

            collection = a.collection;
            a_parent = a_parent ? collection.get(a_parent) : a;
            b_parent = b_parent ? collection.get(b_parent) : b;
            return nestingSort(a_parent, b_parent);
        },
        /*
         * SheetItem Model
         */
        Item = uijet.Model({
            idAttribute : 'id',
            branchName  : function (from_id) {
                var ancestors = this.attributes.ancestors,
                    index = from_id ? ancestors.indexOf(from_id) : null,
                    result = [],
                    ancestors_len = ancestors.length;

                if ( index === null ) {
                    index = 0;
                }
                else if ( ~ index ) {
                    index += 1;
                }

                while ( ancestors_len > index ) {
                    ancestors_len -= 1;
                    result.unshift(this.collection.get(ancestors[ancestors_len]).get('name'));
                }

                return result;
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

                    item.actual = parseFloat(item.actual);
                    item.budget = parseFloat(item.budget);

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
                    return (parent && parent.node) === parent_id;
                });
            },
            byAncestor      : function (ancestor_id) {
                if ( ancestor_id ) {
                    return this.filter(function (item) {
                        return ~ item.attributes.ancestors.indexOf(ancestor_id);
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
        });

    return {
        Item    : Item,
        Items   : Items,
        utils   : {
            reverseSorting  : reverseSorting,
            nestingSort     : nestingSort
        },
        '_'     : _
    };
});
