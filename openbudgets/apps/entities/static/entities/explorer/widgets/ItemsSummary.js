define([
    'uijet_dir/uijet',
    'resources',
    'explorer',
    'uijet_dir/widgets/Base'
], function (uijet, resources, explorer) {

    var formatCommas = uijet.utils.formatCommas;

    uijet.Widget('ItemsSummary', {
        renderContent   : function (scope_item_model) {
            var code = '', direction = '', budget, actual;
            if ( scope_item_model ) {
                code = scope_item_model.get('code');
                direction = scope_item_model.get('direction');
                budget = scope_item_model.get('budget');
                actual = scope_item_model.get('actual');

                budget = budget == null ?
                         '' :
                         formatCommas(budget);

                actual = actual == null ?
                         '' :
                         formatCommas(actual);
            }
            else if ( scope_item_model === null ) {
                var sheet = explorer.getSheetMeta();
                budget = formatCommas(parseInt(sheet.get('budget'), 10));
                actual = formatCommas(parseInt(sheet.get('actual'), 10));
            }
            this.$code.text(code);
            this.$direction.text(direction);
            this.$budget.text(budget);
            this.$actual.text(actual);
        }
    });

});
