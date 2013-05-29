from django.views.generic import DetailView, ListView
from openbudget.apps.entities.models import Domain, Entity


class EntityListView(ListView):
    model = Entity
    template_name = 'entities/entity_list.html'

    def get_context_data(self, **kwargs):
        context = super(EntityListView, self).get_context_data(**kwargs)
        context['object_list'] = Entity.objects.filter(division__index=3).values\
                ('name', 'slug', 'description', 'division__name')
        return context


class EntityDetailView(DetailView):
    model = Entity
    template_name = 'entities/entity_detail.html'
