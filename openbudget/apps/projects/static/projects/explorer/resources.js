define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore',
    'backbone-fetch-cache'
], function (uijet, Backbone, _) {

    uijet.use({
        prop: function (property) {
            return function (obj) {
                return obj[property];
            };
        }
    }, uijet.Utils);

    var
        reverseSorting = function (field) {
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
        /*
         * Muni (Entity) Model
         */
        Muni = uijet.Model({
            idAttribute : 'id'
        }),
        /*
         * Munis (Entities) Collection
         */
        Munis = uijet.Collection({
            model   : Muni,
            parse   : function (response) {
                //! Array.prototype.filter
                return response.results;
            }
        }),
        /*
         * DnormalizedSheetItem Model
         */
        Item = uijet.Model({
            idAttribute : 'id'
        }),
        /*
         * DnormalizedSheetItems Collection
         */
        Items = uijet.Collection({
            model           : Item,
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
                var results = response.results,
                    last = results.length - 1,
                    paths_lookup = {},
                    parent_ids = {},
                    item, n, route, path;
                for ( n = last; item = results[n]; n-- ) {
                    item.ancestors = [];
                    paths_lookup[item.path] = item;
                    if ( item.parent ) {
                        item.parent = item.parent.id || item.parent;
                        if ( ! parent_ids[item.parent] ) {
                            parent_ids[item.parent] = [];
                        }
                        parent_ids[item.parent].push(item.id);
                    }
                }
                for ( n = last; item = results[n]; n-- ) {
                    if ( parent_ids[item.id] ) {
                        item.children = parent_ids[item.id];
                    }
                    else {
                        item.leaf_item = true;
                    }
                    route = item.path.split('|').slice(1);
                    item.level = route.length;
                    while ( route.length ) {
                        path = route.join('|');
                        if ( path in paths_lookup ) {
                            item.ancestors.push(paths_lookup[path].id);
                        }
                        route.shift();
                    }
                }
                paths_lookup = null;
                parent_ids = null;

                return results;
            },
            roots           : function () {
                return this.byParent(null);
            },
            byParent        : function (parent_id) {
                return this.where({
                    parent  : parent_id
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
                        }, this )
                        .sort( function (a, b) {
                            return a.attributes.level - b.attributes.level;
                        } );
                    branch.push(tip_item);
                }
                return branch || [];
            },
            past            : function (item_id, past) {
                var item = this.get(item_id),
                    backwards = item.get('backwards');
                past = past || [];
                _.each(backwards, function (id) {
                    past.push(id);
                    this.past(id, past);
                }, this);
                return past;
            },
            future          : function (item_id, future) {
                var item = this.get(item_id),
                    forwards = item.get('forwards');
                future = future || [];
                _.each(forwards, function (id) {
                    future.push(id);
                    this.future(id, future);
                }, this);
                return future;
            },
            timeline        : function (item_id) {
                return[item_id].concat(this.future(item_id), this.past(item_id));
            }
        });

    return {
        Munis   : Munis,
        Item    : Item,
        Items   : Items,
        utils   : {
            reverseSorting  : reverseSorting
        }
    };
});
