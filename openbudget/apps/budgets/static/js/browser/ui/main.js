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
                process_data    : function (items) {
                    var cache = {}, data = [];

                    items.forEach(function (item, i) {
                        var time = +new Date(item.budget.period_start)/1000;
                        if ( time in cache ) {
                            data[cache[time]].y += item.amount;
                        }
                        else {
                            cache[time] = data.length;
                            data.push({
                                x : time,
                                y : item.amount
                            });
                        }
                    });

                    return data.sort(function (a, b) {
                        return a.x - b.x;
                    });
                },
                draw_timeline   : function (selected) {
                    this.context = {
                        node_pk     : selected.row.attr('data-node'),
                        entity_pk   : app.current_muni.id
                    };
                    this.update().then(function () {
                        this.options.graph.series = [{
                            data    : this.data,
                            color   : this.palette.color()
                        }];
                        this.changed = true;

                        this.wake(true);
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