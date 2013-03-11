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
            type_class  : ['uijet_list', 'uijet_tablerow']
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
            type_class  : ['uijet_list', 'uijet_tablegrid']
        },
        init    : function (options) {
            this._super(options);

            var row_config = this.options.row;

            row_config && uijet.Factory(this.id + '_row', row_config);

            return this;
        },
        render  : function () {
            var res = this._super();

            // init

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

            var table_id = this.id,
                body = this.options.body,
                head = this.options.head;

            // init TableHead
            if ( ! head ) head = {};
                if ( ! head.element ) {
                    head.element = uijet.$('<ul>', { id : table_id + '_head' });
                    this.$element.append(head.element);
                }
                if ( ! head.container ) head.container = table_id;

            uijet.start({
                type    : 'TableHead',
                config  : head
            });

            // init TableGrid
            if ( ! body ) body = {};
                if ( ! body.element ) {
                    body.element = uijet.$('<ul>', { id : table_id + '_grid' });
                    this.$element.append(body.element);
                }
                if ( ! body.container ) body.container = table_id;

            uijet.start({
                type    : 'TableGrid',
                config  : body
            });

            return this;
        },
        render  : function () {
            var res = this._super();
            // render head
            // render body
            return res;
        }
    });

}));