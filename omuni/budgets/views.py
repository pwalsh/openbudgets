from django.views.generic import DetailView
from omuni.budgets.models import Budget, Actual


class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'govts/budget_detail.html'
    slug_field = 'uuid'


class ActualDetailView(DetailView):
    model = Actual
    template_name = 'govts/actual_detail.html'
    slug_field = 'uuid'
