from django.views.generic import DetailView, ListView
from django.utils.translation import ugettext as _
from openbudget.apps.taxonomies.models import Taxonomy, TaxonomyTag, TaxonomyTaggedItem


class TaxonomyDetailView(DetailView):
    model = Taxonomy
    template_name = 'taxonomies/taxonomy_detail.html'


class TaxonomyTagDetailView(DetailView):
    model = TaxonomyTag
    template_name = 'taxonomies/taxonomy_tag_detail.html'
    slug_field = 'unislug'
