from django.contrib.contenttypes import generic
from openbudgets.apps.sources.models import ReferenceSource, AuxSource


class ReferenceSourceInline(generic.GenericStackedInline):
    """Gives an inlineable DataSource form"""

    model = ReferenceSource
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0


class AuxSourceInline(generic.GenericStackedInline):
    """Gives an inlineable DataSource form"""

    model = AuxSource
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0
