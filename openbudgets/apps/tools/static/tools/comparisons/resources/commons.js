define([
    'uijet_dir/uijet',
    'modules/data/backbone',
    'underscore',
    'modules/promises/q'
], function (uijet, Backbone, _) {

    uijet.use({
        prop: function (property) {
            return function (obj) {
                return obj[property];
            };
        }
    }, uijet.utils);

    function sortByPeriod (a, b) {
        return a.period - b.period;
    }

    function addFloats (a, b) {
        var res = a + b;
        return +(res).toPrecision((res | 0).toString().length + 2);
    }

    var
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
         * User (Account) Model
         */
        User = uijet.Model({
            idAttribute: 'uuid',
            name    : function () {
                var first = this.get('first_name'),
                    last = this.get('last_name');
                if ( first || last ) {
                    return first + ' ' + last;
                }
                else {
                    return gettext('Guest');
                }
            },
            avatar  : function () {
                var avatar = this.get('avatar');
                return avatar ? avatar.replace(/s=\d+[^&]/i, 's=90') : window.DEFAULT_AVATAR;
            }
        }),
        /*
         * State Model
         */
        State = uijet.Model({
            parse   : function (response) {
                if ( uijet.utils.isObj(response.author) ) {
                    if ( ! this.has('author_model') ) {
                        response.author_model = new User(response.author);
                    }
                    response.author = response.author.id;
                }
                return response;
            }
        }),
        /*
         * TimeSeries Model
         */
        TimeSeriesModel = uijet.Model({
            parse   : function (response) {
                var periods = [],
                    series = {},
                    missing_periods = [];
                response.forEach(function (item) {
                    var period = +item.period;
                    if ( !~ periods.indexOf(period) ) {
                        periods.push(period);
                    }
                    if ( ! (period in series) ) {
                        series[period] = {
                            budget  : +item.budget,
                            actual  : +item.actual,
                            factor  : 1
                        };
                    }
                    else {
                        series[period].budget = addFloats(series[period].budget, +item.budget);
                        series[period].actual = addFloats(series[period].actual, +item.actual); 
                    }
                });

                periods.sort().forEach(function (period, n) {
                    var current = periods[n - 1] + 1;
                    //TODO: assuming for now that periods is a sequence of years
                    // skip the first and check that each period is the following year of the previous period
                    if ( n && period === current ) {
                        while ( current < period ) {
                            missing_periods.push(current);
                            series[current] = {
                                budget: 0,
                                actual: 0,
                                factor: 1
                            };

                            current += 1;
                        }
                    }
                });
                // missing periods
                periods.push.apply(periods, missing_periods);

                return {
                    periods : periods.sort(),
                    series  : series
                };
            },
            toSeries: function () {
                var series = this.get('series'),
                    actuals = [],
                    budgets = [],
                    period, seria;
                for ( period in series ) {
                    seria = series[period];
                    actuals.push({
                        period  : period,
                        amount  : seria.actual / seria.factor
                    });
                    budgets.push({
                        period  : period,
                        amount  : seria.budget / seria.factor
                    });
                }
                return [actuals.sort(sortByPeriod), budgets.sort(sortByPeriod)];
            }
        });


    return {
        '_'             : _,
        Backbone        : Backbone,
        Muni            : Muni,
        Munis           : Munis,
        User            : User,
        State           : State,
        TimeSeriesModel : TimeSeriesModel
    };
});
