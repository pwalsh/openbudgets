define([
    'uijet_dir/uijet'
], function (uijet) {

    uijet.Adapter('SearchedList', {
        filterItems : function (value) {
            if ( this.has_data && this.$children ) {
                var results = this.search(value),
                    filter = function (i, item) {
                        return ~ results.indexOf(+uijet.$(item).attr('data-id'));
                    };
                this.$children.filter(filter).removeClass('removed');
                this.$children.not(filter).addClass('removed');
                this.publish('filtered');
            }
            else {
                var _self = arguments.callee,
                    rendered_event = this.id + '.rendered';
                if ( 'cached_value' in this ) {
                    this.cached_value = value;
                }
                else {
                    this.cached_value = value;
                    this.subscribe(rendered_event, function () {
                        this.unsubscribe(rendered_event);
                        _self.call(this, this.cached_value);
                        delete this.cached_value;
                    });
                }
            }
            return this;
        }
    });

});
