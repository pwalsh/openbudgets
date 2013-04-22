define([
    'uijet_dir/uijet',
    'importer/app'
], function (uijet, Importer) {

    uijet.declare([{
        type    : 'Pane',
        config  : {
            element : '#heading',
            position: 'top:50'
        }
    }, {
        type    : 'Form',
        config  : {
            element : '#import_form',
            position: 'fluid'
        }
    }]);

    return Importer;

});
