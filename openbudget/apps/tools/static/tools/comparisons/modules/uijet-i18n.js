define([
    'uijet_dir/uijet',
    'i18n',
    'uijet_dir/widgets/Base'
], function (uijet, i18n) {

    var I18N_ATTRIBUTE = 'data-i18n',
        I18N_ATTR_ATTRIBUTE = 'data-i18n-attr',
        normalizeToElement = function (el) {
            if ( el ) {
                if ( typeof el == 'string' ) {
                    return document.querySelector(el);
                }
                else if ( el.nodeType === 1 ) {
                    return el;
                }
                else if ( el[0] && el[0].nodeType === 1 ) {
                    return el[0];
                }
            }
            return null;
        };

    uijet.Mixin('Translated', {
        translated  : true,
        render      : function () {
            return uijet.when(this._super.apply(this, arguments)).then(
                this.translate.bind(this)
            );
        }
    })

    .use({
        _translate  : i18n,
        translate   : function (dfrd) {
            this._translate();
            dfrd && dfrd.resolve();
            return this;
        }
    })
    .use({
        translate   : function () {
            var context = normalizeToElement(this.options.translate_context);
            uijet._translate(context || this.$element[0]);
            return this;
        }
    }, uijet.BaseWidget.prototype)

    // add an init task to parse the DOM for widgets
    .init_queue.push(function (dfrd) {
        this.translate(dfrd);
        return dfrd.promise();
    });
});
