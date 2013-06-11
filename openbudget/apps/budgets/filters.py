from django_filters import FilterSet
from openbudget.apps.budgets.models import Template, Budget, Actual


class TemplateFilter(FilterSet):
    class Meta:
        model = Template


class BudgetFilter(FilterSet):
    class Meta:
        model = Budget


class ActualFilter(FilterSet):
    class Meta:
        model = Actual
