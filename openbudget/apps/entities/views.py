from django.views.generic import DetailView, ListView
from openbudget.apps.entities.models import Domain, Entity


class EntityListView(ListView):
    model = Entity
    template_name = 'entities/entity_list.html'


class EntityDetailView(DetailView):
    model = Entity
    template_name = 'entities/entity_detail.html'
