define([
    'uijet_dir/uijet',
    'common_resources'
], function (uijet, resources) {

    resources.TimeSeries = uijet.Collection({
        model   : resources.TimeSeriesModel,
        periods : function () {
            return this.map(function (seria) {
                return seria.get('periods');
            }).reduce(function (prev, current) {
                current.forEach(function (item) {
                    if ( !~ this.indexOf(item) )
                        this.push(item);
                }, prev);
                return prev;
            }).sort();
        }
    });

    return resources;

});
