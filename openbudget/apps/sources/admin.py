from django.contrib.contenttypes import generic
from openbudget.apps.sources.models import DataSource


class DataSourceInline(generic.GenericStackedInline):
    """Gives an inlineable DataSource form"""

    model = DataSource
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0
