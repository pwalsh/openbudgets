define([
    'uijet_dir/uijet',
    'resources/budget'
], function (uijet) {

    uijet.declare([{
        type    : 'Table',
        config  : {
            element : '#spreadsheet',
            head    : {
                columns : ['code', 'name', 'amount', 'description']
            },
            body    : {
                mixins          : ['Templated'],
                resource        : 'Budget',
                template_name   : 'spreadsheet-body'
            }
        }
    }]);

});