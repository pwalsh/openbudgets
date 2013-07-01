define([
    'uijet_dir/uijet',
    'uijet_dir/widgets/Button'
], function (uijet) {

    uijet.Widget('ContentEditable', {
        options         : {
            type_class  : ['uijet_contenteditable'],
            wrapper_tag : 'span',
            dont_wrap   : false
        },
        prepareElement  : function () {
            this._super.apply(this, arguments)
                ._wrap();

            var input_ops = this.options.input;

            this.$input = uijet.$('<input>', {
                type        : 'text',
                name        : input_ops.name,
                placeholder : this.$element.text(),
                'class'     : 'uijet_contenteditable_input hide'
            }).appendTo(this.$wrapper);

            this.$input.on('blur', this.blur.bind(this));

            return this;
        },
        click           : function () {
            this.$element.addClass('hide');
            this.$input.removeClass('hide')
                .focus();
            return this;
        },
        blur            : function () {
            var value = this.$input.addClass('hide').val();

            this.$element.text(value || this.$input.attr('placeholder'));
            this.$element.removeClass('hide');

            this.publish('updated', value);

            return this;
        }
    }, {
        widgets : ['Button']
    });

});
