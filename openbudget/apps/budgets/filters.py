from django_filters import FilterSet
from openbudget.apps.budgets import models


class TemplateFilter(FilterSet):

    class Meta:
        model = models.Template
        fields = ['divisions', 'using_sheets']


class TemplateNodeFilter(FilterSet):

    class Meta:
        model = models.TemplateNode
        fields = ['templates', 'direction', 'parent', 'children', 'inverse']


class SheetFilter(FilterSet):

    class Meta:
        model = models.Sheet
        fields = ['entity', 'template']


class SheetItemFilter(FilterSet):

    class Meta:
        model = models.SheetItem
        fields = ['sheet', 'sheet__entity', 'node', 'node__code',
                  'node__direction', 'node__parent', 'node__children']
