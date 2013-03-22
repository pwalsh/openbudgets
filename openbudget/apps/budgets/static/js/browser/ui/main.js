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
                        this.$element[0].style.opacity = 0;
                    },
                    post_rowsinit   : function () {
                        this.$element[0].style.opacity = 1;
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
            graph       : {
                renderer: 'stack',
                scheme  : 'classic9',
                axis    : 'time'
            },
            data_url    : app.BASE_API_URL + '{entity_pk}/timeline/{node_pk}/',
            signals     : {
                process_data    : function (items) {
                    return items.map(function (item) {
                        return {
                            x : new Date(item.budget.period_start).getFullYear(),
                            y : item.amount
                        };
                    }).sort(function (a, b) {
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