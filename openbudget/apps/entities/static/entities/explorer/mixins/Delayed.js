define([
    'uijet_dir/uijet'
], function (uijet) {

    uijet.Mixin('Delayed' ,{
        delay   : function (fn, milis, data) {
            var handler = this._parseHandler(fn);
            this.delay_handle = setTimeout(
                data === void 0 ?
                    handler.bind(this) :
                    handler.bind(this, data),
                milis
            );
            return this;
        },
        cancel  : function () {
            clearTimeout(this.delay_handle);
            return this;
        },
        instead : function (fn, milis, data) {
            if ( this.delay_handle ) {
                this.cancel();
            }
            return this.delay(fn, milis, data);
        }
    });

});
