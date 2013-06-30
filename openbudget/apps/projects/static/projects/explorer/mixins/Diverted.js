define([
    'uijet_dir/uijet'
], function (uijet) {

    uijet.Mixin('Diverted', {
        wake: function (context) {
            if ( context && this.id in context ) {
                this[context[this.id]]();
                return this;
            }
            else {
                return this._super.apply(this, arguments);
            }
        }
    });

});
