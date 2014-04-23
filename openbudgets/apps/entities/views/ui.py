from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from openbudgets.apps.accounts.serializers import AccountMin
from openbudgets.apps.entities.models import Entity
from openbudgets.apps.sheets.models import Sheet, SheetItem
from openbudgets.apps.contexts.models import Context
from openbudgets.apps.sheets.serializers import SheetItem as SheetItemSerializer
from openbudgets.apps.sheets.serializers import Sheet as SheetSerializer
from openbudgets.commons.utilities import commas_format


class EntityDetailUISerializer(serializers.ModelSerializer):

    sheets = SheetSerializer()

    class Meta:
        model = Entity
        fields = ['id', 'name', 'description', 'code', 'sheets', 'slug']


class EntityList(ListView):
    model = Entity
    queryset = model.objects.related_map().filter(division__index=3)
    template_name = 'entities/entity_list.html'

    def get_context_data(self, **kwargs):
        context = super(EntityList, self).get_context_data(**kwargs)
        entities_active = []
        entities_inactive = []

        for e in self.object_list:
            if e.sheets.exists():
                entities_active.append(e)
            else:
                entities_inactive.append(e)

        context['entities_active'] = entities_active
        context['entities_inactive'] = entities_inactive

        return context


class EntityDetail(DetailView):
    model = Entity
    template_name = 'entities/explorer.html'

    def get_context_data(self, **kwargs):
        context = super(EntityDetail, self).get_context_data(**kwargs)
        period = self.kwargs.get('period', None)
        node_id = self.kwargs.get('node_id', None)

        sheets = []
        items_list = {}
        renderer = JSONRenderer()
        sheet = None
        scope_item = None
        user = self.request.user
        user_object = {}
        contextual_data = {}

        # add logged in user
        if user.is_authenticated():
            user_object = AccountMin(user).data

        context['user_json'] = renderer.render(user_object)
        context['contextual_data'] = Context.objects.latest_of(entity_id=self.object.id)

        # add sheets data
        if self.object.sheets.exists():

            if period:
                try:
                    #TODO: this assumes period is always a year, but need to refactor to use settings.OPENBUDGET_PERIOD_RANGES
                    sheet = Sheet.objects.get(entity=self.object.id, period_start__year=period)
                except Sheet.DoesNotExist:
                    sheet = Sheet.objects.latest_of(self.object.id)
            else:
                sheet = Sheet.objects.latest_of(self.object.id)

            if node_id:
                try:
                    scope_item = SheetItem.objects.get_queryset().get(sheet=sheet, node=node_id)
                    items = scope_item.children.order_by('node__code')
                except SheetItem.DoesNotExist:
                    items = sheet.items.filter(node__parent__isnull=True).order_by('node__code')
            else:
                items = sheet.items.filter(node__parent__isnull=True).order_by('node__code')

            items_list = SheetItemSerializer(items, many=True, context={'request': self.request}).data

            for s in self.object.sheets.all():
                sheets.append({
                    'id': unicode(s.id),
                    'period': s.period
                })

        context['sheets'] = sheets
        context['object_json'] = renderer.render(EntityDetailUISerializer(self.object, context={'request': self.request}).data)
        context['sheet'] = sheet
        context['sheet_json'] = renderer.render(SheetSerializer(sheet, context={'request': self.request}).data) if sheet else '{}'

        # format numbers in items_list
        for item in items_list:
            item['direction'] = _(item['direction'])
            budget = item['budget']
            actual = item['actual']

            if budget is None:
                item['f_budget_empty'] = True
                item['f_budget'] = ''
            else:
                item['f_budget'] = commas_format(budget)

            if actual is None:
                item['f_actual_empty'] = True
                item['f_actual'] = ''
            else:
                item['f_actual'] = commas_format(actual)

        context['items_list_json'] = renderer.render(items_list)

        # rendering initial state of breadcrumbs
        # setting initial scope name
        if scope_item:
            scope_item_serialized = SheetItemSerializer(scope_item, context={'request': self.request}).data

            # format numbers
            scope_item_serialized['budget'] = commas_format(scope_item_serialized['budget'])
            scope_item_serialized['actual'] = commas_format(scope_item_serialized['actual'])

            # translate direction
            scope_item_serialized['direction'] = _(scope_item_serialized['direction'])

            context['scope_item_json'] = renderer.render(scope_item_serialized)

            # breadcrumbs
            crumbs = scope_item_serialized['ancestors'] + [{
                'name': scope_item_serialized['name'],
                'node': scope_item_serialized['node']
            }]

            context['items_breadcrumbs'] = render_to_string('items_breadcrumbs.ms', {
                'stache': crumbs
            })

            context['scope_item'] = scope_item_serialized
            context['scope_name'] = scope_item_serialized['name']
        else:
            context['scope_item_json'] = '{}'
            context['items_breadcrumbs'] = ''
            context['scope_item'] = {
                'actual': commas_format(sheet.actual),
                'budget': commas_format(sheet.budget),
                'direction': '',
                'code': ''
            }
            context['scope_name'] = _('Main')

        # rendering initial state of the items table
        context['items_list'] = render_to_string('items_list.ms', {
            'stache': items_list
        })
        return context
