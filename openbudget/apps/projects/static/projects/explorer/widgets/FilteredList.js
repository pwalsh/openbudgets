define([
    'uijet_dir/uijet',
    'uijet_dir/widgets/List'
], function (uijet) {

    uijet.Widget('FilteredList', {
        init        : function (options) {
            var method_prefix = 'filterBy',
                filter;

            this.cached_values = {};
            this.filters_map = options.filters;
            for ( filter in this.filters_map ) {
                if ( typeof this.filters_map[filter] == 'string' ) {
                    this.filters_map[filter] = this[filter];
                }
                this[method_prefix + filter[0].toUpperCase() + filter.slice(1)] = this.filterItems.bind(this, filter);
            }

            return this._super.apply(this, arguments);
        },
        filterItems : function (filter_name, value) {
            var results, filter;
            if ( filter_name ) {
                if ( this.has_data && this.$children ) {
                    if ( value === null ) {
                        delete this.cached_values[filter_name];
                        results = null;
                    }
                    else {
                        this.cached_values[filter_name] = value;
                        results = this.filters_map[filter_name].call(this, value);
                    }
                    this.filterChildren(results, filter_name);
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
                    for ( filter in this.cached_values )
                        this.filterItems(filter, this.cached_values[filter]);
                }
            }
            return this;
        },
        filterChildren  : function (ids, prefix) {
            var class_name = this.options.removed_class || 'removed',
                filter;
            if ( prefix )
                class_name = prefix + '_' + class_name;
            if ( ids === null ) {
                this.$children.removeClass(class_name);
            }
            else {
                filter = function (i, item) {
                    return ~ ids.indexOf(+uijet.$(item).attr('data-id'));
                };
                this.$children.filter(filter).removeClass(class_name);
                this.$children.not(filter).addClass(class_name);
            }
            this.publish('filtered');
            return this;
        },
        queueFilter     : function (filter_name, value) {
            if ( this.queued_filters ) {
                if ( value === null ) {
                    delete this.cached_values[filter_name];
                }
                else {
                    this.cached_values[filter_name] = value;
                }
            }
            else {
                var rendered_event = this.id + '.rendered';
                this.queued_filters = true;

                this.cached_values[filter_name] = value;

                this.subscribe(rendered_event, function () {
                    var filter;
                    this.unsubscribe(rendered_event);
                    for ( filter in this.cached_values ) {
                        this.filterItems(filter, this.cached_values[filter]);
                    }
                    this.queued_filters = false;
                });
            }
        }
    }, {
        widgets : 'List'
    });

});
