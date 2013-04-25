define([
    'uijet_dir/uijet',
    'uijet_dir/modules/dom/jquery',
    'uijet_dir/modules/pubsub/eventbox',
    'uijet_dir/modules/promises/q',
    'uijet_dir/modules/engine/mustache',
    'uijet_dir/modules/xhr/jquery'
], function (uijet, $, Ebox, Q, Mustache) {

    function getCSRFToken () {
        return document.cookie.match(CSRF_TOKEN_RE)[1];
    }

    var CSRF_TOKEN_RE = /csrftoken=([a-zA-Z0-9]+)/,
        Importer =  {
            BASE_API_URL: window.BASE_API_URL,
            UPLOAD_URL  : window.UPLOAD_URL,
            start   : function (options) {
                /*
                 * Subscribe to events in views
                 */
                uijet.subscribe({
                    'import_form.submitted'         : function (data) {
                        var form_data = new FormData(),
                            attributes = 'name=' + data.name + ';divisions=' + data.divisions.join(',');

                        form_data.append('sourcefile', data.file);
                        form_data.append('type', 'budgettemplate');
                        form_data.append('email', data.email);
                        form_data.append('attributes', attributes);

                        Importer.upload(form_data)
                            .then(function (value) {
                                console.log('Upload finished', value);
                            }, function (reason) {
                                console.error(reason);
                            });
                    }
                });
                /*
                 * Starting uijet
                 */
                uijet.init({
                    element             : '#importer',
                    templates_path      : '/static/src/importer/templates/',
                    templates_extension : 'ms'
                });
            },
            upload  : function (form_data) {
                //TODO: doesn't work on IE9-, need to polyfill with some plugin
                return uijet.xhr(this.UPLOAD_URL, {
                    type        : 'POST',
                    data        : form_data,
                    processData : false,
                    contentType : false,
                    headers     : {
                        'X-CSRFToken'   : getCSRFToken()
                    }
                });
            }
        };

    return Importer;
});
