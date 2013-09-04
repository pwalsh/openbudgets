define([
    'uijet_dir/uijet',
    'uijet_dir/widgets/Button'
], function (uijet) {

    var default_key = 'default';

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
            
            this.$input = uijet.$('<input>', uijet.utils.extend({
                type        : 'text',
                placeholder : this.$element.text(),
                'class'     : 'uijet_contenteditable_input hide'
            }, input_ops)).appendTo(this.$wrapper);

            this.$input.on({
                blur    : this.blur.bind(this),
                keyup   : this.keyup.bind(this)
            });

            return this;
        },
        destroy         : function () {
            this.$input.off();
            this.$input = null;
            return this._super.apply(this, arguments);
        },
        reset     : function (value, silent) {
            this.change(value, silent)
                .$input.val(value);
            return this;
        },
        change          : function (value, silent) {
            //! String.prototype.trim
            value = value.trim();
            this.$element.text(value || this.$input.attr('placeholder'));
            this.last_value = value;
            silent || this.publish('updated', value);
            return this;
        },
        click           : function () {
            this.$element.addClass('hide');
            this.$input.removeClass('hide')
                .focus();
            return this;
        },
        blur            : function () {
            var value;

            if ( this.cancelled ) {
                this.cancelled = false;
                value = this.last_value || '';
                this.$input.addClass('hide').val(value);
            }
            else {
                value = this.$input.addClass('hide').val();
            }

            this.$element.removeClass('hide');

            return this.change(value);
        },
        keyup           : function (e) {
            var key = e.keyCode || e.which,
                keys = this.options.keys;

            if ( keys ) {
                if ( uijet.utils.isFunc(keys[key]) )
                    return keys[key].call(this, e);
                else if ( uijet.utils.isFunc(keys[default_key]) )
                    return keys[default_key].call(this, e);
            }

            // enter
            if ( key === 13 ) {
                this.$input.blur();
            }
            // esc key
            else if ( key === 27 ) {
                this.cancelled = true;
                this.$input.blur();
            }
        }
    }, {
        widgets : ['Button']
    });

});
