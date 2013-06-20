define([
    'uijet_dir/uijet',
    'uijet_dir/widgets/Button'
], function (uijet) {

    uijet.Widget('LegendItem', {
        options     : {
            type_class  : ['legend_item']
        },
        render      : function () {
            var res = this._super.apply(this, arguments),
                $buttons = this.$element.find('.legend_item_buttons'),
                button_class_prefix = '.legend_item_',
                id = this.id;

            uijet.start([{
                type    : 'Button',
                config  : {
                    element     : $buttons.find(button_class_prefix + 'color'),
                    id          : id + '_color',
                    container   : id
                }
            }, {
                type    : 'Button',
                config  : {
                    element     : $buttons.find(button_class_prefix + 'edit'),
                    id          : id + '_edit',
                    container   : id
                }
            }, {
                type    : 'Button',
                config  : {
                    element     : $buttons.find(button_class_prefix + 'duplicate'),
                    id          : id + '_duplicate',
                    container   : id
                }
            }, {
                type    : 'Button',
                config  : {
                    element     : $buttons.find(button_class_prefix + 'delete'),
                    id          : id + '_delete',
                    container   : id
                }
            }], true);

            this.subscribe(id + '_color.clicked', this.itemColor)
                .subscribe(id + '_edit.clicked', this.itemEdit)
                .subscribe(id + '_duplicate.clicked', this.itemDuplicate)
                .subscribe(id + '_delete.clicked', this.itemDelete);

            return res;
        },
        itemColor       : function () {},
        itemEdit        : function () {
            uijet.publish('legends_list.selected', this.options.index);
        },
        itemDuplicate   : function () {
            uijet.publish('legends_list.duplicate', this.options.index);
        },
        itemDelete      : function () {
            uijet.publish('legends_list.delete', this.options.index);
            this.destroy();
        }
    });

});
