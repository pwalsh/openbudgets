from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import DetailView, ListView
from django.utils.translation import ugettext as _
from django.shortcuts import render
from openbudget.apps.budgets.models import Budget, BudgetItem, Actual, ActualItem, Template
from openbudget.apps.entities.models import Entity
from openbudget.settings import base as settings


class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'budgets/budget_detail.html'
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


class ActualDetailView(DetailView):
    model = Actual
    template_name = 'budgets/actual_detail.html'
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


class BudgetItemDetailView(DetailView):
    model = BudgetItem
    template_name = 'budgets/budget_item_detail.html'
    slug_field = 'uuid'


class ActualItemDetailView(DetailView):
    model = ActualItem
    template_name = 'budgets/actual_item_detail.html'
    slug_field = 'uuid'


class BudgetListView(ListView):
    model = Budget
    template_name = 'budgets/budget_list.html'


class ActualListView(ListView):
    model = Actual
    template_name = 'budgets/actual_list.html'


class BudgetTemplateListView(ListView):
    model = Template
    template_name = 'budgets/template_list.html'


class BudgetTemplateDetailView(DetailView):
    model = Template
    template_name = 'budgets/template_detail.html'
    slug_field = 'uuid'


def budget_browser(request):
    return render(request, 'budgets/browser.html')
