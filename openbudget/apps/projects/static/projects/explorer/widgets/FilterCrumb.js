define([
    'uijet_dir/uijet',
    'uijet_dir/widgets/Button'
], function (uijet) {

    uijet.Widget('FilterCrumb', {
        options     : {
            type_class  : 'uijet_filtercrumb'
        },
        init        : function () {
            this._super.apply(this, arguments);

            this.$content = uijet.$('<span>', {
                'class' : 'filter_content',
                text    : this.options.content || ''
            }).appendTo(this.$element);


            var x_button_id = this.id + '_remove';

            uijet.start(uijet.utils.extend(true, {
                type    : 'Button',
                config  : {
                    element     : uijet.$('<span>', {
                        id      : x_button_id,
                        'class' : 'filtercrumb_remove'
                    }).appendTo(this.$element),
                    id          : x_button_id,
                    container   : this.id
                }
            }, this.options.button || {}));

            return this;
        },
        setContent  : function (content) {
            this.$content.text(content);
            return this;
        }
    });

});
