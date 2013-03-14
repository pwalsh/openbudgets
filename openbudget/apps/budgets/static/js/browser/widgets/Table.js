;(function (factory) {
    if ( typeof define === 'function' && define.amd ) {
        define([
            'uijet_dir/uijet',
            'uijet_dir/widgets/List'
        ], function (uijet) {
            return factory(uijet);
        });
    } else {
        factory(uijet);
    }
}(function (uijet) {

    /**
     * @name TableRow
     * @extends List
     * 
     * Used with @see Table widget.
     */
    uijet.Widget('TableRow', {
        options : {
            type_class  : ['uijet_list', 'uijet_tablerow'],
            horizontal  : true
        }
    }, {
        widgets : 'List'
    })

    /**
     * @name TableHead
     * @extends TableRow
     * 
     * Used with @see Table widget.
     */
    .Widget('TableHead', {
        options : {
            type_class  : ['uijet_list', 'uijet_tablerow', 'uijet_tablehead']
        }
    }, {
        widgets : 'TableRow'
    })

    /**
     * @name TableGrid
     * @extends List
     * @requires TableRow
     * 
     * Used with @see Table widget.
     * Implemented as a @see List of @see TableRow widgets.
     */
    .Widget('TableGrid', {
        options : {
            type_class      : ['uijet_list', 'uijet_tablegrid'],
            item_selector   : '.uijet_tablerow'
        },
        init    : function (options) {
            this._super(options);
            this.row_factory_id = this.id + '_row';

            var row = this.options.row || {};
            if ( ! row.container ) row.container = this.id;

            uijet.Factory(this.row_factory_id, {
                type    : 'TableRow',
                config  : row
            });

            return this;
        },
        render  : function () {
            var res = this._super(),
                factory_id = this.row_factory_id;

            // init rows
            this.$element.children().each(function (i, row) {
                uijet.start({
                    factory : factory_id,
                    config  : {
                        element : row
                    }
                });
            });

            return res;
        }
    }, {
        widgets : 'List'
    })

    /**
     * @name Table
     * @extends BaseWidget
     * @requires TableHead
     * @requires TableGrid
     */
    .Widget('Table', {
        options : {
            type_class  : 'uijet_table'
        },
        init    : function (options) {
            this._super(options);

            this.initHead(this.options.head)
                .initGrid(this.options.grid);

            return this;
        },
        initHead: function (options) {
            var table_id = this.id;
            // init TableHead
            if ( ! options ) options = {};
            if ( ! options.element ) {
                options.element = uijet.$('<ul>', { id : table_id + '_head' });
                this.$element.append(options.element);
            }
            if ( ! options.container ) options.container = table_id;

            uijet.start({
                type    : 'TableHead',
                config  : options
            });
            return this;
        },
        initGrid: function (options) {
            var table_id = this.id;
            // init TableGrid
            if ( ! options ) options = {};
            if ( ! options.element ) {
                options.element = uijet.$('<ul>', { id : table_id + '_grid' });
                this.$element.append(options.element);
            }
            if ( ! options.container ) options.container = table_id;

            uijet.start({
                type    : 'TableGrid',
                config  : options
            });
            return this;
        }
    });

}));