define([
    'uijet_dir/uijet',
    'uijet_dir/widgets/List'
], function (uijet) {

    uijet.Widget('FilteredList', {
        init                : function (options) {
            var method_prefix = 'filterBy',
                flag = 1,
                filter;

            this.filter_flags = {};
            this.active_filters = 0;
            this.cached_values = {};
            this.cached_results = {};
            this.filters_map = options.filters;
            for ( filter in this.filters_map ) {
                this.filter_flags[filter] = flag;
                if ( typeof this.filters_map[filter] == 'string' ) {
                    this.filters_map[filter] = this[filter];
                }
                this[method_prefix + filter[0].toUpperCase() + filter.slice(1)] = this.filterItems.bind(this, filter);
                flag = flag << 1;
            }

            return this._super.apply(this, arguments);
        },
        updateFlags         :function (flags) {
            var new_state = 0,
                flag, value;
            for ( flag in flags ) {
                if ( flag in this.filter_flags ) {
                    value = !!flags[flag];
                    value && (new_state |= this.filter_flags[flag]);
                }
            }
            this.active_filters = new_state;
            return this;
        },
        runFilter           : function (filter_name, value) {
            var results = null;
            if ( value === null ) {
                this.clearFilter(filter_name);
            }
            else {
                if ( arguments.length == 2 ) {
                    this.cached_values[filter_name] = value;
                }
                else {
                    value = this.cached_values[filter_name];
                }

                this.cached_results[filter_name] = results = this.filters_map[filter_name].call(this, value);
                this.active_filters |= this.filter_flags[filter_name];
            }
            return results;
        },
        filterItems         : function (filter_name, value) {
            var filter;
            if ( filter_name ) {
                if ( this.has_data && this.$children ) {
                    this.runFilter(filter_name, value);
                }
                else {
                    this.queueFilter(filter_name, value);
                }
            }
            else {
                if ( this.queued_filters ) {
                    this.publish('rendered');
                }
                else {
                    for ( filter in this.cached_values ) {
                        this.runFilter(filter);
                    }
                }
            }
            return this;
        },
        clearFilter         : function (name) {
            this.active_filters &= ~this.filter_flags[name];
            delete this.cached_values[name];
            delete this.cached_results[name];
            return this;
        },
        filterChildren      : function () {
            var class_name = 'removed',
                ids, filter;
            if ( ! this.active_filters ) {
                this.$children.removeClass(class_name);
                this.$last_filter_result = this.$children;
            }
            else {
                ids = this._intersectResults();

                if ( ! ids.length ) {
                    this.$children.addClass(class_name);
                    this.$last_filter_result = null;
                }
                else {
                    filter = function (i, item) {
                        return ~ ids.indexOf(uijet.$(item).attr('data-id'));
                    };
                    this.$last_filter_result = this.$children.filter(filter).removeClass(class_name);
                    this.$children.not(filter).addClass(class_name);
                }
            }
            this.notify('post_filtered', ids || null);
            return this;
        },
        queueFilter         : function (filter_name, value) {
            if ( this.queued_filters ) {
                if ( value === null ) {
                    this.clearFilter(filter_name);
                }
                else {
                    this.cached_values[filter_name] = value;
                    this.active_filters |= this.filter_flags[filter_name];
                }
            }
            else {
                this.queued_filters = true;

                this.cached_values[filter_name] = value;
                this.active_filters |= this.filter_flags[filter_name];
            }
        },
        _intersectResults   : function () {
            var result = [],
                has_single_results = false,
                name, prev_name;
            // kind of Array.reduce for Objects
            for ( name in this.cached_results ) {
                if ( ! prev_name ) {
                    prev_name = name;
                    // this ensures that we at least return results if there's a single set in cache
                    has_single_results = true;
                    continue;
                }
                has_single_results = false;

                this.cached_results[name].forEach(function (id) {
                    if ( ~ this.indexOf(id) )
                        result.push(id);
                }, result.length ? result : this.cached_results[prev_name]);
            }
            return has_single_results ? this.cached_results[name] : result;
        }
    }, {
        widgets : 'List'
    });

});
