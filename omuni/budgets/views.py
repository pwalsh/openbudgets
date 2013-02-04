from django.views.generic import DetailView
from omuni.budgets.models import Budget


class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'govts/budget_detail.html'
    slug_field = 'uuid'
