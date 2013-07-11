define([
    'uijet_dir/uijet',
    'dictionary'
], function (uijet, dictionary) {

    var I18N_ATTRIBUTE = 'data-i18n',
        I18N_ATTR_ATTRIBUTE = 'data-i18n-attr';

    uijet.use({
        translate   : function (dfrd) {
            if ( dictionary ) {
                uijet.$('[' + I18N_ATTRIBUTE + ']').each(function (i, el) {
                    var $el = uijet.$(el),
                        translation = dictionary[$el.attr(I18N_ATTRIBUTE)],
                        attr = $el.attr(I18N_ATTR_ATTRIBUTE);
                    translation && (attr ? $el.attr(attr, translation) : $el.text(translation));
                });
            }
            dfrd && dfrd.resolve();
            return this;
        }
    })

    // add an init task to parse the DOM for widgets
    .init_queue.push(function (dfrd) {
        this.translate(dfrd);
        return dfrd.promise();
    });
});
