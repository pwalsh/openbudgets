from django.views.generic import DetailView, ListView
from openbudget.govts.models import GeoPoliticalEntity


class GeoPolListView(ListView):
    model = GeoPoliticalEntity
    template_name = 'govts/geopol_list.html'


class GeoPolDetailView(DetailView):
    model = GeoPoliticalEntity
    template_name = 'govts/geopol_detail.html'

    # TODO: get object when slug is more complex
    # We want things like:
    # /state/country/budget/year
    # /state/country
    # /state/country/budget/year
    # /state/country/actual/year
    # couldn't get it working in a clean way with a nice API.

    #def get_object(self, queryset=None):
    #    print 'get object'
    #    real_slug = self.kwargs['slug'].split(',')[-1]
    #    print real_slug
    #    queryset = super(GeoPolDetailView, self).get_queryset()
    #    print queryset
    #    queryset = queryset.filter(slug=real_slug)
    #    print 'this'
    #    print queryset
    #    obj = super(GeoPolDetailView, self).get_object(queryset)
    #    return obj
