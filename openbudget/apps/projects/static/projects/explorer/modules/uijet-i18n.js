define([
    'uijet_dir/uijet',
    'dictionary',
    'uijet_dir/widgets/Base'
], function (uijet, dictionary) {

    var I18N_ATTRIBUTE = 'data-i18n',
        I18N_ATTR_ATTRIBUTE = 'data-i18n-attr';

    uijet.Mixin('Translated', {
        translated  : true,
        render      : function () {
            return uijet.when(this._super.apply(this, arguments)).then(
                this.translate.bind(this)
            );
        }
    })

    .use({
        _translate  : function (context) {
            if ( dictionary ) {
                uijet.$('[' + I18N_ATTRIBUTE + ']', context || document).each(function (i, el) {
                    var $el = uijet.$(el),
                        translation = dictionary[$el.attr(I18N_ATTRIBUTE)],
                        attr = $el.attr(I18N_ATTR_ATTRIBUTE);
                    translation && (attr ? $el.attr(attr, translation) : $el.text(translation));
                });
            }
        },
        translate   : function (dfrd) {
            this._translate();
            dfrd && dfrd.resolve();
            return this;
        }
    })
    .use({
        translate   : function () {
            uijet._translate(this.options.translate_context || this.$element);
            return this;
        }
    }, uijet.BaseWidget.prototype)

    // add an init task to parse the DOM for widgets
    .init_queue.push(function (dfrd) {
        this.translate(dfrd);
        return dfrd.promise();
    });
});
