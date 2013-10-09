from haystack import indexes
from openbudgets.apps.sheets import models


class SheetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    period_start = indexes.DateField(model_attr='period_start')
    period_end = indexes.DateField(model_attr='period_end')

    def get_model(self):
        return models.Sheet


class SheetItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.SheetItem
