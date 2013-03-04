from django.views.generic import DetailView
from openbudget.budgets.models import Budget, BudgetItem, Actual, ActualItem


class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'budgets/budget_detail.html'
    slug_field = 'uuid'


class ActualDetailView(DetailView):
    model = Actual
    template_name = 'budgets/actual_detail.html'
    slug_field = 'uuid'


class BudgetItemDetailView(DetailView):
    model = BudgetItem
    template_name = 'budgets/budget_item_detail.html'
    slug_field = 'uuid'


class ActualItemDetailView(DetailView):
    model = ActualItem
    template_name = 'budgets/actual_item_detail.html'
    slug_field = 'uuid'
