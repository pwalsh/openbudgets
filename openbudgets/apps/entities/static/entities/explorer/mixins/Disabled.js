define([
    'uijet_dir/uijet'
], function (uijet) {

    uijet.Mixin('Disabled' ,{
        disable     : function () {
            this.disabled = true;
            this.$element.addClass('disabled');
            return this;
        },
        enable      : function () {
            this.disabled = false;
            this.$element.removeClass('disabled');
            return this;
        }
    });

});
