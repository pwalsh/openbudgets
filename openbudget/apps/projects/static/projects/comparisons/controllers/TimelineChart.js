define([
    'uijet_dir/uijet',
    'resources',
    'api'
], function (uijet, resources, api) {

    var period_start = 'period_start';

    function sortByPeriod (a, b) { return a.period - b.period; }
    function sortByPeriodstart (a, b) {
        return new Date(a.get(period_start)) > new Date(b.get(period_start)) ? 1 : -1;
    }
    function addFloats (a, b) {
        var res = a + b;
        return +(res).toPrecision((res | 0).toString().length + 2);
    }

    /**
     * Gets the latest context that has a `period_start` that precedes the period
     * or is equal to it.
     * 
     * This function has a side-effect of reducing `contexts` by shifting items
     * if their preceding item's `period_start` is before `period`.
     * 
     * @param {Array} contexts - list of Context model instances
     * @param {String} period - a string representation of a date
     * @returns {Object|undefined} - latest context to use for this period's series
     */
    function latestContextForPeriod (contexts, period) {
        var context, period_to_date;
        if ( contexts.length ) {
            if ( contexts.length === 1 ) {
                context = contexts[0];
            }
            else {
                period_to_date = new Date(period);
                context = contexts[0];
                if ( new Date(context.get(period_start)) <= period_to_date &&
                     new Date(contexts[1].get(period_start)) <= period_to_date ) {
    
                    contexts.shift();
                    return latestContextForPeriod(contexts, period);
                }
            }
        }
        return context;
    }

    var TimeSeriesModel = uijet.Model({
        url         : function () {
            return api.getTimelineRoute(this.attributes.muni_id, this.attributes.nodes);
        },
        parse       : function (response) {
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
                    series[period].budget = addFloats(series[period].budget, +item.budget);
                    series[period].actual = addFloats(series[period].actual, +item.actual); 
                }
            });
            return {
                periods : periods.sort(),
                series  : series
            };
        },
        toSeries    : function () {
            var series = this.normalize(),
                actuals = [],
                budgets = [],
                period, seria;
            for ( period in series ) {
                seria = series[period];
                actuals.push({
                    period  : period,
                    amount  : seria.actual
                });
                budgets.push({
                    period  : period,
                    amount  : seria.budget
                });
            }
            return [actuals.sort(sortByPeriod), budgets.sort(sortByPeriod)];
        },
        normalize   : function () {
            var normalize_by = uijet.Resource('NodesListState').get('normalize_by'),
                series = this.get('series'),
                result = {},
                contexts;

            if ( normalize_by ) {
                contexts = uijet.Resource('Contexts')
                    .where({ entity : this.get('muni_id') });
                if ( contexts.length )
                    contexts.sort(sortByPeriodstart);
                else
                    return series;
            }
            else {
                return series;
            }

            //TODO: assuming here period is a "full year"
            this.get('periods').forEach(function (period) {
                var seria = series[period],
                    context, factor;

                context = latestContextForPeriod(contexts, period);
                factor = context ? +context.get('data')[normalize_by] : 1;

                // cache last calculated factor for State serialization
                seria.factor = factor;

                result[period] = {
                    budget  : seria.budget / factor,
                    actual  : seria.actual / factor
                };
            });

            return result;
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
                    title       : attrs.title,
                    placeholder : attrs.title || gettext('Insert title'),
                    nodes       : attrs.nodes,
                    muni        : new resources.Muni({
                        id  : attrs.muni_id,
                        name: attrs.muni
                    }),
                    amount_type : attrs.amount_type,
                    color       : attrs.color
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

            return this.resource.set(updated_models).fetch();
        }
    });

});
