define([
    'uijet_dir/uijet',
    'browser/app'
], function (uijet) {

    var BASE_API_URL = 'http://api.obudget.dev:8000/',
        BudgetModel = uijet.Model({
            idAttribute : 'uuid'
        }),
        BudgetsCollection = uijet.Collection({
            model   : BudgetModel,
            url     : BASE_API_URL + 'budgets/',
            parse   : function (response) {
                return response.results;
            }
        }),
        exports = {
            budget_model        : BudgetModel,
            budgets_collection  : BudgetsCollection
        };

    uijet.Resource('Budgets', BudgetsCollection);

    return exports;
});