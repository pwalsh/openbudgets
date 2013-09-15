define([
    'uijet_dir/uijet'
], function (uijet) {

    uijet.Adapter('TimelineChart', {
        set : function (legend_item_models) {
            var updated_models = legend_item_models.map(function (legend_item) {
                var muni = legend_item.get('muni'),
                    muni_id = muni.id,
                    nodes = legend_item.get('nodes'),
                    title = legend_item.get('title'),
                    type = legend_item.get('amount_type'),
                    color = legend_item.get('color'),
                    muni_name = muni.get('name'),
                    model = this.resource.get(legend_item.cid),
                    now = Date.now();

                if ( model ) {
                    model.set({
                        muni_id     : muni_id,
                        nodes       : nodes,
                        title       : title,
                        muni        : muni_name,
                        amount_type : type,
                        color       : color
                    });
                    if ( model.hasChanged() ) {
                        model.set({ updated : now });
                    }
                }
                else {
                    model = new TimeSeriesModel({
                        id          : legend_item.id,
                        muni_id     : muni_id,
                        nodes       : nodes,
                        title       : title,
                        muni        : muni_name,
                        amount_type : type,
                        color       : color,
                        updated     : now
                    });
                }
                return model;
            }, this);

            return this.resource.set(updated_models)
                .fetch()
                .then(function () {
                    return uijet.Resource('NodesListState').get('normalize_by') && this.resource.recalcFactors();
                }.bind(this));
        }
    });

});
