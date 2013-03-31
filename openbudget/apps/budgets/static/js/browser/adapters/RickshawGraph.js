;(function (factory) {
    if ( typeof define === 'function' && define.amd ) {
        define([
            'uijet_dir/uijet',
            'rickshaw'
        ], function (uijet, Rickshaw) {
            return factory(uijet, Rickshaw);
        });
    } else {
        factory(uijet, Rickshaw);
    }
}(function (uijet, Rickshaw) {

    uijet.Adapter('RickshawGraph', {
        setGraphOptions : function (ops) {
            this.axes = {};

            if ( ! ops )
                this.options.graph = ops = {};

            if ( ! ops.element )
                ops.element = this.$element[0];

            if ( ops.scheme ) {
                this.palette = new Rickshaw.Color.Palette({ scheme: ops.scheme });
                delete ops.scheme;
            }
            if ( ops.x_axis ) {
                this.axes.x = ops.x_axis;
                delete ops.x_axis;
            }
            if ( ops.y_axis ) {
                this.axes.y = ops.y_axis;
                delete ops.y_axis;
            }

            return this;
        },
        initGraph       : function (graph_data) {
            if ( ! this.graph ) {
                var ops = this.options.graph,
                    x_axis, y_axis;

                if ( graph_data )
                    ops.series = graph_data;

                if ( ops.series ) {
                    this.graph = new Rickshaw.Graph(ops);
                    if ( x_axis = this.axes.x ) {
                        if ( x_axis === 'time' )
                            new Rickshaw.Graph.Axis.Time({ graph: this.graph });
                        else
                            new Rickshaw.Graph.Axis.X({ graph: this.graph });
                    }
                    if ( y_axis = this.axes.y ) {
                        new Rickshaw.Graph.Axis.Y({ graph: this.graph });
                    }
                }
                else {
                    var that = this;
                    return uijet.when(this.getGraphData()).then(function () {
//                        that.initGraph(that.data);
                    }, uijet.Utils.rethrow);
                }
            }
            return this;
        },
        draw            : function (graph_data) {
            var that = this;
            if ( this.changed ) {
                this.changed = false;
                delete this.graph;
                this.clear();
            }
            if ( this.graph ) {
                this.graph.render();
            }
            else {
                uijet.when( this.initGraph(graph_data) )
                    .then(function () {
                       that.draw(); 
                    }, uijet.Utils.rethrow);
            }
            return this;
        },
        clear           : function () {
            this.$element.empty();
            return this;
        }
    });

}));