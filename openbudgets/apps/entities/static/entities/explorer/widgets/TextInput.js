define([
    'uijet_dir/uijet',
    'uijet_dir/widgets/Button'
], function (uijet) {

    var default_key = 'default';

    uijet.Widget('TextInput', {
        options         : {
            type_class  : ['uijet_textinput'],
            dom_events  : {
                keyup   : 'keyup+'
            },
            // force wrapping
            position    : true
        },
        clear           : function () {
            this.$element.val('').focus();
            return this;
        },
        keyup           : function (e) {
            var key = e.keyCode || e.which,
                keys = this.options.keys;

            if ( keys ) {
                if ( uijet.utils.isFunc(keys[key]) )
                    return keys[key].call(this, e);
                else if ( uijet.utils.isFunc(keys[default_key]) ) {
                    return keys[default_key].call(this, e);
                }
            }
        }
    })
});
