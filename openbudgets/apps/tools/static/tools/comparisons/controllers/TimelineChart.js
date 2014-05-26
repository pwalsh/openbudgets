define([
    'uijet_dir/uijet',
    'resources'
], function (uijet, resources) {

    uijet.Adapter('TimelineChart', {
        set : function (legend_item_models) {
            var updated_models = legend_item_models.map(function (legend_item) {
                var attrs = legend_item.attributes,
                    muni = attrs.muni,
                    muni_id = muni.id,
                    nodes = attrs.nodes,
                    title = attrs.title,
                    type = attrs.amount_type,
                    color = attrs.color,
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
                    model = new resources.TimeSeriesModel({
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

            this.resource.set(updated_models);

            return this.resource.fetch()
                .then(function () {
                    return uijet.Resource('NodesListState').get('normalize_by') && this.resource.recalcFactors();
                }.bind(this));
        }
    });

});
