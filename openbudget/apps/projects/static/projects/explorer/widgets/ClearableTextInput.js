define([
    'uijet_dir/uijet',
    'uijet_dir/widgets/Button'
], function (uijet) {

    var default_key = 'default';

    uijet.Widget('ClearableTextInput', {
        options         : {
            type_class  : ['uijet_clearabletextinput'],
            dom_events  : {
                keyup  : 'keyup+'
            }
        },
        prepareElement  : function () {
            var ret = this._super(),
                button_ops = this.options.button || {};

            this._wrap();

            uijet.start({
                type    : 'Button',
                config  : uijet.Utils.extend(true, {
                    element     : button_ops.element || uijet.$('<span>', {
                        id : this.id + '_clear'
                    }).appendTo(this.$wrapper),
                    container   : this.id,
                    extra_class : 'uijet_clear_button'
                }, button_ops)
            });

            this.subscribe(this.id + '_clear.clicked', 'clear');

            return ret;
        },
        clear           : function () {
            this.$element.val('').focus();
            return this;
        },
        keyup           : function (e) {
            var key = e.keyCode || e.which,
                keys = this.options.keys;

            if ( keys ) {
                if ( uijet.Utils.isFunc(keys[key]) )
                    return keys[key].call(this, e);
                else if ( uijet.Utils.isFunc(keys[default_key]) ) {
                    return keys[default_key].call(this, e);
                }
            }
        }
    })
});
