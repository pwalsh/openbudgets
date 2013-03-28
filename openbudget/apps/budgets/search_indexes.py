import datetime
from haystack import indexes
from openbudget.apps.budgets.models import Budget, BudgetItem, Actual, ActualItem


class BudgetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    period_start = indexes.DateField(model_attr='period_start')
    period_end = indexes.DateField(model_attr='period_end')

    def get_model(self):
        return Budget


class ActualIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    period_start = indexes.DateField(model_attr='period_start')
    period_end = indexes.DateField(model_attr='period_end')

    def get_model(self):
        return Actual


class BudgetItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return BudgetItem


class ActualItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ActualItem
