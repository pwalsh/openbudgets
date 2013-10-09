from django.views.generic import DetailView
from openbudgets.apps.sources.models import AuxSource, ReferenceSource


class AuxSourceDetailView(DetailView):
    model = AuxSource
    template_name = 'sources/auxsource_detail.html'


class ReferenceSourceDetailView(DetailView):
    model = ReferenceSource
    template_name = 'sources/referencesource_detail.html'
