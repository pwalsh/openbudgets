define([
    'uijet_dir/uijet',
    'browser/app',
    'widgets/Table',
    'widgets/Graph',
    'adapters/RickshawGraph'
], function (uijet, app) {

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
        type    : 'Table',
        config  : {
            element     : '#spreadsheet',
            dont_wake   : true,
            mixins      : ['Layered'],
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
    }, {
        type    : 'Graph',
        config  : {
            element     : '#graph',
            adapters    : 'RickshawGraph',
            mixins      : ['Layered'],
            dont_wake   : true,
            graph       : {
                renderer: 'stack',
                scheme  : 'classic9',
                axis    : 'time'
            },
            position    : 'fluid',
            data_url    : app.BASE_API_URL + '{entity_pk}/timeline/{node_pk}/',
            signals     : {
                process_data: function (items) {
                    return items.map(function (item) {
                        return {
                            x : new Date(item.budget.period_start).getFullYear(),
                            y : item.amount
                        };
                    }).sort(function (a, b) {
                        return a.x - b.x;
                    });
                }
            },
            app_events  : {
                'spreadsheet.selected'  : function (selected) {
                    this.context = {
                        node_pk     : selected.row[0].id,
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
            }
        }
    }]);

    return app;
});