import datetime
from haystack import indexes
from openbudgets.apps.entities.models import Entity


class EntityIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Entity
