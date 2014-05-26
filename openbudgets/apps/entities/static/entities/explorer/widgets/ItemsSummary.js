define([
    'uijet_dir/uijet',
    'resources',
    'uijet_dir/widgets/Base'
], function (uijet, resources) {

    var formatCommas = uijet.utils.formatCommas;

    uijet.Widget('ItemsSummary', {
        renderContent   : function (scope_item_model) {
            var roots, code = '', direction = '', budget, actual;
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
                roots = uijet.Resource('LatestSheet').roots();
                budget = formatCommas(
                    roots.length ?
                        roots.reduce(function (prev, current) {
                            return (typeof prev == 'number' ? prev : prev.get('budget') | 0) + current.get('budget') | 0;
                        }) :
                        0
                );
                actual = formatCommas(
                    roots.length ?
                        roots.reduce(function (prev, current) {
                            return (typeof prev == 'number' ? prev : prev.get('actual') | 0) + current.get('actual') | 0;
                        }) :
                        0
                );
            }
            this.$code.text(code);
            this.$direction.text(direction);
            this.$budget.text(budget);
            this.$actual.text(actual);
        }
    });

});
