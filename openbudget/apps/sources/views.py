from django.views.generic import DetailView
from django.utils.translation import ugettext as _
from openbudget.apps.sources.models import AuxSource, ReferenceSource


class AuxSourceDetailView(DetailView):
    model = AuxSource
    template_name = 'sources/auxsource_detail.html'
    slug_field = 'uuid'


class ReferenceSourceDetailView(DetailView):
    model = ReferenceSource
    template_name = 'sources/referencesource_detail.html'
    slug_field = 'uuid'
