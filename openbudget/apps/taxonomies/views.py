
from django.views.generic import DetailView, ListView
from django.utils.translation import ugettext as _
from openbudget.apps.taxonomies.models import Taxonomy, Tag


class TaxonomyDetailView(DetailView):
    model = Taxonomy
    template_name = 'taxonomies/taxonomy_detail.html'


class TagDetailView(DetailView):
    model = Tag
    template_name = 'taxonomies/tag_detail.html'
