define([
    'uijet_dir/uijet',
    'resources',
    'api'
], function (uijet, resources, api) {

    function sortByPeriod (a, b) { return a.period - b.period; }

    var TimeSeriesModel = uijet.Model({
        url : function () {
            return api.getTimelineRoute(this.attributes.muni_id, this.attributes.nodes);
        },
        parse   : function (response) {
            var periods = [],
                series = {};
            response.forEach(function (item) {
                var period = +item.period;
                if ( !~ periods.indexOf(period) ) {
                    periods.push(period);
                }
                if ( ! (period in series) ) {
                    series[period] = {
                        budget  : +item.budget,
                        actual  : +item.actual
                    };
                }
                else {
                    series[period].budget += +item.budget;
                    series[period].actual += +item.actual; 
                }
            });
            return {
                periods : periods.sort(),
                series  : series
            };
        },
        toSeries: function () {
            var series = this.get('series'),
                actuals = [],
                budgets = [],
                period;
            for ( period in series ) {
                actuals.push({
                    period  : period,
                    amount  : series[period].actual
                });
                budgets.push({
                    period  : period,
                    amount  : series[period].budget
                });
            }
            return [actuals.sort(sortByPeriod), budgets.sort(sortByPeriod)];
        }
    });

    uijet.Resource('TimeSeries', uijet.Collection({
        model           : TimeSeriesModel,
        fetch           : function () {
            return uijet.whenAll(this.models.map(function (model) {
                return model.fetch();
            }));
        },
        periods         : function () {
            return this.pluck('periods').reduce(function (prev, current) {
                current.forEach(function (item) {
                    if ( !~ this.indexOf(item) )
                        this.push(item);
                }, prev);
                return prev;
            }).sort();
        },
        extractLegend   : function () {
            return this.models.map(function (model) {
                var attrs = model.attributes;
                return {
                    title   : attrs.title,
                    nodes   : attrs.nodes,
                    muni    : new resources.Muni({
                        id  : attrs.muni_id,
                        name: attrs.muni
                    })
                };
            });
        }
    }));

    uijet.Adapter('TimelineChart', {
        set : function (legend_item_models) {
            var updated_models = legend_item_models.map(function (legend_item) {
                var muni = legend_item.get('muni'),
                    muni_id = muni.id,
                    nodes = legend_item.get('nodes'),
                    title = legend_item.get('title'),
                    type = legend_item.get('amount_type'),
                    muni_name = muni.get('name'),
                    model = this.resource.get(legend_item.cid),
                    now = Date.now();

                if ( model ) {
                    model.set({
                        muni_id     : muni_id,
                        nodes       : nodes,
                        title       : title,
                        muni        : muni_name,
                        amount_type : type
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
                        updated     : now
                    });
                }
                return model;
            }, this);

            return this.resource.set(updated_models).fetch();
        }
    });

});
