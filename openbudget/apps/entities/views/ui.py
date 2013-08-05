from django.views.generic import DetailView, ListView
from openbudget.apps.entities.models import Entity


class EntityList(ListView):
    model = Entity
    template_name = 'entities/entity_list.html'

    def get_context_data(self, **kwargs):
        context = super(EntityList, self).get_context_data(**kwargs)
        #TODO: change this now we have new manager
        context['object_list'] = Entity.objects.filter(division__index=3).values\
                ('name', 'slug', 'description', 'division__name')
        return context


class EntityDetail(DetailView):
    model = Entity
    template_name = 'entities/explorer.html'

    def get_context_data(self, **kwargs):
        context = super(EntityDetail, self).get_context_data(**kwargs)
        context['periods'] = self.object.periods
        return context
