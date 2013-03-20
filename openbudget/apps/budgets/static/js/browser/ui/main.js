define([
    'uijet_dir/uijet',
    'resources/budget',
    'widgets/Graph',
    'adapters/RickshawGraph'
], function (uijet) {

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#heading',
            position: 'top:50'
        }
    }, {
        type    : 'List',
        config  : {
            element : '#budgets_list',
            mixins  : ['Templated'],
            resource: 'Budgets',
            position: 'top:70|50',
            signals : {
                pre_select  : function ($selected) {
                    return this.resource.get($selected[0].id).toJSON();
                }
            }
        }
    }, {
        type    : 'Table',
        config  : {
            element     : '#spreadsheet',
            dont_wake   : true,
            mixins      : ['Layered'],
            head        : {
                columns : ['code', 'name', 'amount', 'description']
            },
            grid        : {
                mixins          : ['Templated'],
                template_name   : 'spreadsheet-grid',
                signals         : {
                    pre_render      : function () {
                        this.$element[0].style.opacity = 0;
                    },
                    post_rowsinit   : function () {
                        this.$element[0].style.opacity = 1;
                    }
                },
                app_events      : {
                    'budgets_list.selected' : function (data) {
                        this.data = data;
                        this.publish('wake', true);
                    }
                }
            },
            position    : 'fluid',
            app_events  : {
                'spreadsheet_grid.wake' : 'wake+'
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
            resource    : 'Budgets',
            app_events  : {
                'spreadsheet.selected'  : function (selected) {
                    var data = this.resource.chartData(selected.row.index());
                    this.options.graph.series = [{
                        data    : data,
                        color   : this.palette.color()
                    }];
                    this.changed = true;

                    this.wake(true);
                }
            }
        }
    }]);

});