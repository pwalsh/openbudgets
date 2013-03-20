;(function (factory) {
    if ( typeof define === 'function' && define.amd ) {
        define([
            'uijet_dir/uijet',
            'uijet_dir/widgets/Base'
        ], function (uijet) {
            return factory(uijet);
        });
    } else {
        factory(uijet);
    }
}(function (uijet) {

    uijet.Widget('Graph', {
        options : {
            type_class  : ['uijet_pane', 'uijet_graph']
        },
        setInitOptions  : function () {
            this.setGraphOptions(this.options.graph);
            return this._super();
        },
        render          : function () {
            var res = this._super();

            if ( ! this.options.dont_draw )
                this.draw();

            return res;
        },
        setGraphOptions : function (ops) {
            return this;
        },
        getGraphData    : function () {
            return this.update();
        },
        draw            : function () {
            return this;
        },
        clear           : function () {
            return this;
        }
    });

}));