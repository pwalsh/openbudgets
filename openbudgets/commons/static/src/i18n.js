define(['dictionary'], function (dictionary) {

    var I18N_ATTRIBUTE = 'data-i18n',
        I18N_ATTR_ATTRIBUTE = 'data-i18n-attr',
        I18N_SAFE_ATTRIBUTE = 'data-i18n-safe',
        use_textContent = 'textContent' in document.body;

    return function (context) {
        if ( dictionary ) {

            var selection = (context || document).querySelectorAll('[' + I18N_ATTRIBUTE + ']');

            Array.prototype.forEach.call(selection, function (el) {
                var translation = dictionary[el.getAttribute(I18N_ATTRIBUTE)],
                    attr = el.getAttribute(I18N_ATTR_ATTRIBUTE);
                if ( translation ) {
                    if ( attr ) {
                        el.setAttribute(attr, translation);
                    }
                    else {
                        if ( el.hasAttribute(I18N_SAFE_ATTRIBUTE) ) {
                            el.innerHTML = translation;
                        }
                        else {
                            if ( use_textContent ) {
                                el.textContent = translation;
                            }
                            else {
                                el.innerText = translation;
                            }
                        }
                    }
                }
            });

        }
    };
});
