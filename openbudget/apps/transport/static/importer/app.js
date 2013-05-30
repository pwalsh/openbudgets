define([
    'uijet_dir/uijet',
    'controllers/Upload',
    'uijet_dir/modules/dom/jquery',
    'uijet_dir/modules/pubsub/eventbox',
    'uijet_dir/modules/promises/q',
    'uijet_dir/modules/engine/mustache',
    'uijet_dir/modules/xhr/jquery'
], function (uijet, UploadController, $, Ebox, Q, Mustache) {

    var Importer =  {
            BASE_API_URL: window.BASE_API_URL,
            start   : function (options) {
                /*
                 * Subscribe to events in views
                 */
                uijet.subscribe({
                    'import_form.submitted' : UploadController.doImport
                });
                /*
                 * Starting uijet
                 */
                uijet.init({
                    element             : '#importer',
                    templates_path      : '/static/importer/templates/',
                    templates_extension : 'ms',
                    dont_cover          : true
                });
            }
        };

    return Importer;
});
