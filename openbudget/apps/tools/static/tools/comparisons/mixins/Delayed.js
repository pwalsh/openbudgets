define([
    'uijet_dir/uijet'
], function (uijet) {

    uijet.Mixin('Delayed' ,{
        delay   : function (fn, delay, data) {
            var handler = this._parseHandler(fn);

            handler = data === void 0 ?
                    handler.bind(this) :
                    handler.bind(this, data);

            this.delay_handle = setTimeout(handler, delay);
            return this;
        },
        cancel  : function () {
            clearTimeout(this.delay_handle);
            return this;
        },
        instead : function (fn, delay, data) {
            if ( this.delay_handle ) {
                this.cancel();
            }
            return this.delay(fn, delay, data);
        }
    });

});
