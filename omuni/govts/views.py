from django.views.generic import DetailView, ListView
from omuni.govts.models import GeoPoliticalEntity


class GeoPolListView(ListView):
    model = GeoPoliticalEntity
    template_name = 'govts/geopol_list.html'

    def get_context_data(self, **kwargs):
        context = super(GeoPolListView, self).get_context_data(**kwargs)
        print context
        return context


class GeoPolDetailView(DetailView):
    model = GeoPoliticalEntity
    template_name = 'govts/geopol_detail.html'
