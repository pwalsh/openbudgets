import datetime
from haystack import indexes
from openbudget.apps.budgets.models import Budget, Actual


class BudgetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Budget


class ActualIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Actual
