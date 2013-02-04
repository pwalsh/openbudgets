from django.views.generic import DetailView, ListView
from omuni.govts.models import GeoPoliticalEntity


class GeoPolListView(ListView):
    model = GeoPoliticalEntity
    template_name = 'govts/geopol_list.html'


class GeoPolDetailView(DetailView):
    model = GeoPoliticalEntity
    template_name = 'govts/geopol_detail.html'
