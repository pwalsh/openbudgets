from django_filters import FilterSet, NumberFilter
from openbudget.apps.budgets.models import Template, TemplateNode, Budget,\
    BudgetItem, Actual, ActualItem


class TemplateFilter(FilterSet):

    class Meta:
        model = Template
        fields = ['divisions', 'budgets', 'actuals']


class TemplateNodeFilter(FilterSet):

    class Meta:
        model = TemplateNode
        fields = ['templates', 'direction', 'parent', 'children', 'inverse']


class BudgetFilter(FilterSet):

    class Meta:
        model = Budget
        fields = ['entity', 'template']


class BudgetItemFilter(FilterSet):

    class Meta:
        model = BudgetItem
        fields = ['budget', 'budget__entity', 'node', 'node__code',
                  'node__direction', 'node__parent', 'node__children']


class ActualFilter(FilterSet):

    class Meta:
        model = Actual
        fields = ['entity', 'template']


class ActualItemFilter(FilterSet):

    class Meta:
        model = ActualItem
        fields = ['actual', 'actual__entity', 'node', 'node__code',
                  'node__direction', 'node__parent', 'node__children']
