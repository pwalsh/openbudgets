from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import DetailView, ListView
from django.utils.translation import ugettext as _
from django.shortcuts import render
from openbudget.apps.budgets import models
from openbudget.apps.entities.models import Entity
from openbudget.settings import base as settings


def budget_browser(request):
    return render(request, 'budgets/browser.html')


class TemplateList(ListView):
    model = models.Template
    template_name = 'budgets/template_list.html'


class TemplateDetail(DetailView):
    model = models.Template
    template_name = 'budgets/template_detail.html'
    slug_field = 'uuid'


class SheetList(ListView):
    model = models.Sheet
    template_name = 'budgets/sheet_list.html'


class SheetDetail(DetailView):
    model = models.Sheet
    template_name = 'budgets/sheet_detail.html'
    slug_field = 'uuid'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()

        entity = Entity.objects.get(slug=self.kwargs['entity_slug'])
        ranges = settings.OPENBUDGET_PERIOD_RANGES

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
    template_name = 'budgets/sheet_item_detail.html'
    slug_field = 'uuid'
