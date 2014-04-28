from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import DetailView, ListView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from openbudgets.apps.sheets import models
from openbudgets.apps.entities.models import Entity


def budget_browser(request):
    return render(request, 'sheets/browser.html')


class TemplateList(ListView):
    model = models.Template
    template_name = 'sheets/template_list.html'


class TemplateDetail(DetailView):
    model = models.Template
    template_name = 'sheets/template_detail.html'
    slug_field = 'uuid'


class SheetList(ListView):
    model = models.Sheet
    template_name = 'sheets/sheet_list.html'


class SheetDetail(DetailView):
    model = models.Sheet
    template_name = 'sheets/sheet_detail.html'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()

        entity = Entity.objects.get(slug=self.kwargs['entity_slug'])
        ranges = settings.OPENBUDGETS_PERIOD_RANGES

        # TODO: Support other ranges than yearly, including multiple ranges.
        # fragile, but works with current use case.
        if len(ranges) == 1 and 'yearly' in ranges:
            try:
                obj = queryset.get(entity=entity,
                                      period_start__year=self.kwargs['period'])
            except ObjectDoesNotExist:
                raise Http404(_("No {name} found matching the query").format(
                              name=queryset.model._meta.verbose_name))
        return obj


class SheetItemDetail(DetailView):
    model = models.SheetItem
    template_name = 'sheets/sheet_item_detail.html'


class TemplateNodeDetail(DetailView):
    model = models.TemplateNode
    template_name = 'sheets/template_node_detail.html'

