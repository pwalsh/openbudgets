define([
    'uijet_dir/uijet',
    'browser/app'
], function (uijet) {

    var BASE_API_URL = 'http://api.obudget.dev:8000/',
        BudgetModel = uijet.Model({
            idAttribute : 'uuid'
        }),
        BudgetsCollection = uijet.Collection({
            model       : BudgetModel,
            url         : BASE_API_URL + 'budgets/',
            parse       : function (response) {
                return response.results;
            },
            chartData   : function (index) {
                var budgets = this.toJSON(),
                    data = [];

                budgets.forEach(function (budget) {
                    var time = new Date(budget.period_start).getFullYear();
                    data.push({
                        x : time,
                        y : budget.items[index].amount
                    });
                });

                return data.sort(function (a, b) {
                    return a.x - b.x;
                });
            }
        }),
        exports = {
            budget_model        : BudgetModel,
            budgets_collection  : BudgetsCollection
        };

    uijet.Resource('Budgets', BudgetsCollection);

    return exports;
});