define([
    'uijet_dir/uijet'
], function (uijet) {

    function getCSRFToken () {
        return document.cookie.match(CSRF_TOKEN_RE)[1];
    }

    var CSRF_TOKEN_RE = /csrftoken=([a-zA-Z0-9]+)/,

    UploadController = {
        UPLOAD_URL  : window.UPLOAD_URL,
        doImport    : function (data) {
            var form_data = new FormData(),
                attributes = '';

            switch ( data.type ) {
                case 'template':
                    attributes += 'name=' + data.name +
                                    ';period_start=' + data.period_start +
                                    ';divisions=' + uijet.Utils.toArray(data.divisions).join(',');
                    break;
                case 'sheet':
                    attributes += 'period_start=' + data.period_start +
                                  ';period_end=' + data.period_end +
                                  ';entity=' + data.entity;
                    break;
            }

            if ( ! attributes )
                throw new Error('Source type not selected.');

            form_data.append('sourcefile', data.file);
            form_data.append('type', data.type);
            form_data.append('attributes', attributes);

            UploadController.upload(form_data)
                .then(function (message) {
                    console.log('Upload finished', message);
                    uijet.publish('upload.done', message);
                }, function (jqXHR) {
                    try {
                        var messages = [];
                        data = JSON.parse(jqXHR.responseText);
                        // make messages unique
                        data = data.filter(function (item) {
                            if ( ~ messages.indexOf(item.message) ) {
                                return false;
                            }
                            else {
                                messages.push(item.message);
                                return true;
                            }
                        });
                    } catch (e) {
                        data = [{ message : gettext('Disturbance in the force.') }]
                    }
                    uijet.publish('upload.failed', data);
                });
        },
        upload  : function (form_data) {
            //TODO: FormData not supported on IE9-, need to polyfill with some plugin
            return uijet.xhr(UploadController.UPLOAD_URL, {
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

    return UploadController;
});
