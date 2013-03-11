from django.views.generic import DetailView, ListView
from openbudget.apps.entities.models import Entity


class EntityListView(ListView):
    model = Entity
    template_name = 'entities/entity_list.html'


class EntityDetailView(DetailView):
    model = Entity
    template_name = 'entities/entity_detail.html'

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
    #    queryset = super(EntityDetailView, self).get_queryset()
    #    print queryset
    #    queryset = queryset.filter(slug=real_slug)
    #    print 'this'
    #    print queryset
    #    obj = super(EntityDetailView, self).get_object(queryset)
    #    return obj
