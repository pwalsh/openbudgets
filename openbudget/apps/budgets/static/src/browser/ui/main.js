define([
    'uijet_dir/uijet',
    'browser/app',
    'widgets/Table',
    'widgets/Graph',
    'adapters/RickshawGraph'
], function (uijet, app) {

    uijet.Factory('spreadsheet', {
        type    : 'Table',
        config  : {
            dont_wake   : true,
            grid        : {
                mixins          : ['Templated'],
                resource        : 'Budgets',
                template_name   : 'spreadsheet-grid',
                signals         : {
                    pre_render      : function () {
                        this.disappear();
                    },
                    post_rowsinit   : function () {
                        this.appear();
                    }
                }
            },
            position    : 'fluid',
            app_events  : {
                MUNI_PICKED : 'wake+'
            }
        }
    });

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#heading',
            position: 'top:50'
        }
    }, {
        type    : 'List',
        config  : {
            element : '#munis_list',
            mixins  : ['Templated'],
            resource: 'Munis',
            position: 'top:80|50',
            signals : {
                pre_select  : function ($selected) {
                    return {
                        url : $selected.attr('data-url'),
                        id  : $selected[0].id
                    };
                }
            }
        }
    }, {
        factory : 'spreadsheet',
        config  : {
            element : '#actuals_spreadsheet',
            position: 'bottom:40%',
            grid    : {
                resource: 'Actuals'
            }
        }
    }, {
        factory : 'spreadsheet',
        config  : {
            element : '#budgets_spreadsheet'
        }
    }, {
        type    : 'Graph',
        config  : {
            element     : '#graph',
            adapters    : 'RickshawGraph',
            dont_wake   : true,
            style       : {
                padding : '5%',
                zIndex  : -1
            },
            graph       : {
                renderer: 'line',
                scheme  : 'classic9',
                y_axis  : true,
                x_axis  : 'time'
            },
            data_url    : app.BASE_API_URL + '{entity_pk}/timeline/{node_pk}/',
            signals     : {
                process_data    : function (response) {
                    var items_sorter = function (a, b) {
                            return a.x - b.x;
                        },
                        items_looper = function (item, i) {
                            var time = +new Date((item.actual || item.budget).period_start)/1000;
                            if ( time in cache ) {
                                this[cache[time]].y += item.amount;
                            }
                            else {
                                cache[time] = this.length;
                                this.push({
                                    x : time,
                                    y : item.amount
                                });
                            }
                        },
                        series = [], items = [], cache, type;

                    for ( type in response ) {
                        cache = {};
                        response[type].forEach(items_looper, items);
                        series.push({ data : items.slice().sort(items_sorter) });
                        items.length = 0;
                    }

                    return series;
                },
                get_series      : function () {
                    return (this.options.graph.series = this.getData().map(function (item) {
                        item.color = this.palette.color();
                        return item;
                    }, this));
                },
                draw_timeline   : function (selected) {
                    var context;
                    if ( selected ) {
                        context = this.context = {
                            node_pk     : selected.row.attr('data-node'),
                            entity_pk   : app.current_muni.id,
                            refresh     : true
                        };
                    }
                    this.update().then(function () {
                        this.notify('get_series');
                        this.changed = true;

                        selected && this.wake(context);
                    }.bind(this));
                }
            },
            app_events  : {
                'budgets_spreadsheet.selected'  : 'draw_timeline+',
                'actuals_spreadsheet.selected'  : 'draw_timeline+'
            }
        }
    }]);

    return app;
});