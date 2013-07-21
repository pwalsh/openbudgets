define([
    'uijet_dir/uijet',
    'project_widgets/ContentEditable'
], function (uijet) {

    uijet.Widget('LegendItem', {
        options     : {
            type_class  : ['legend_item']
        },
        init        : function () {
            this._super.apply(this, arguments);
            var id = this.id;

            this.subscribe(id + '_edit.clicked', this.itemEdit)
                .subscribe(id + '_duplicate.clicked', this.itemDuplicate)
                .subscribe(id + '_delete.clicked', this.itemDelete)
                .subscribe(id + '_remove.clicked', this.itemDelete)
                .subscribe(id + '_title.updated', this.updateTitle);

            return this;
        },
        render      : function () {
            var res = this._super.apply(this, arguments),
                $buttons = this.$element.find('.legend_item_buttons'),
                button_class_prefix = '.legend_item_',
                $title = this.$element.find(button_class_prefix + 'title'),
                id = this.id,
                slider_id = id + '_slider',
                in_picker_view = this.options.picking;

            this.setColor();

            uijet.start([{
                type    : 'ContentEditable',
                config  : {
                    element     : $title,
                    id          : id + '_title',
                    container   : id,
                    input       : {
                        name: 'title'
                    }
                }
            }, {
                type    : 'Button',
                config  : {
                    element     : this.$element.find(button_class_prefix + 'remove'),
                    id          : id + '_remove',
                    container   : id,
                    dont_wake   : ! in_picker_view,
                    app_events      : {
                        'nodes_picker.awake'    : 'wake',
                        'chart_reset'           : 'sleep',
                        'picker_done.clicked'   : 'sleep'
                    }
                }
            }, {
                type    : 'Pane',
                config  : {
                    element         : $buttons,
                    id              : slider_id,
                    container       : id,
                    dont_wrap       : true,
                    dont_wake       : in_picker_view,
                    app_events      : {
                        'picker_done.clicked'   : 'wake',
                        'chart_reset'           : 'wake',
                        'nodes_picker.awake'    : 'sleep'
                    }
                }
            }, {
                type    : 'Button',
                config  : {
                    element     : $buttons.find(button_class_prefix + 'edit'),
                    id          : id + '_edit',
                    container   : slider_id
                }
            }, {
                type    : 'Button',
                config  : {
                    element     : $buttons.find(button_class_prefix + 'duplicate'),
                    id          : id + '_duplicate',
                    container   : slider_id
                }
            }, {
                type    : 'Button',
                config  : {
                    element     : $buttons.find(button_class_prefix + 'delete'),
                    id          : id + '_delete',
                    container   : slider_id
                }
            }], true);

            this.wakeContained();

            this.notify(true, 'post_full_render');

            return res;
        },
        setColor        : function (color) {
            if ( color )
                this.options.color = color;
            else
                color = this.options.color;

            this.$element.find('.legend_item_color').css('backgroundColor', color);
            return this;
        },
        itemEdit        : function () {
            uijet.publish('legends_list.selected', this.resource.collection.indexOf(this.resource));
        },
        itemDuplicate   : function () {
            uijet.publish('legends_list.duplicate', this.resource.collection.indexOf(this.resource));
        },
        itemDelete      : function () {
            uijet.publish('legends_list.delete', this.resource.collection.indexOf(this.resource));
            this.destroy();
        },
        updateTitle     : function (title) {
            this.resource.set({ title : title });
        },
        enable          : function () {
            this.disabled = false;
            this.$element.removeClass('disabled');
            return this;
        },
        disable         : function () {
            this.disabled = true;
            this.$element.addClass('disabled');
            return this;
        }
    });

});
