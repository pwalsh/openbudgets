from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import DetailView
from django.utils.translation import ugettext_lazy as _
from openbudgets.apps.taxonomies.models import Taxonomy, Tag


class TaxonomyDetailView(DetailView):
    model = Taxonomy
    template_name = 'taxonomies/taxonomy_detail.html'


class TagDetailView(DetailView):
    model = Tag
    template_name = 'taxonomies/tag_detail.html'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(slug=self.kwargs['slug'])
        taxonomy = Taxonomy.objects.get(slug=self.kwargs['taxonomy_slug'])
        try:
            obj = queryset.get(taxonomy=taxonomy)
        except ObjectDoesNotExist:
            raise Http404(_("No {verbose_name} found matching the query").format(
                verbose_name=queryset.model._meta.verbose_name))
        return obj
