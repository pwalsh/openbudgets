from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from openbudget.apps.accounts.serializers import AccountMin
from openbudget.apps.entities.models import Entity
from openbudget.apps.sheets.models import Sheet, SheetItem
from openbudget.apps.contexts.models import Context
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.sheets.serializers.ui import SheetUISerializer, SheetItemUISerializer
from openbudget.commons.utilities import commas_format


class EntityDetailUISerializer(serializers.ModelSerializer):

    sheets = SheetUISerializer()

    class Meta:
        model = Entity
        fields = ['id', 'name', 'description', 'code', 'sheets', 'slug']\
                 + translated_fields(model)


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
        item_uuid = self.kwargs.get('item_uuid', None)

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

        #TODO: refactor the code below into a generic utility in contexts app that returns the I18N'ised data
        # add latest contextual data objcet for this entity
        try:
            contextual_temp = Context.objects.latest_of(entity_id=self.object.id).data
            for k, v in contextual_temp.iteritems():
                contextual_data[Context.KEYS[k]] = v
        except Context.DoesNotExist:
            pass

        context['contextual_data'] = contextual_data

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

            if item_uuid:
                try:
                    scope_item = SheetItem.objects.get_queryset().get(uuid=item_uuid)
                    items = sheet.sheetitems.filter(node__parent=scope_item.node).order_by('node__code')
                except SheetItem.DoesNotExist:
                    items = sheet.sheetitems.filter(node__parent__isnull=True).order_by('node__code')
            else:
                items = sheet.sheetitems.filter(node__parent__isnull=True).order_by('node__code')

            items_list = SheetItemUISerializer(items, many=True).data

            for s in self.object.sheets.all():
                sheets.append({
                    'id': s.id,
                    'period': s.period,
                    'uuid': str(s.uuid)
                })

        context['sheets'] = sheets
        context['object_json'] = renderer.render(EntityDetailUISerializer(self.object).data)
        context['sheet'] = sheet
        context['sheet_json'] = renderer.render(SheetUISerializer(sheet).data) if sheet else '{}'

        # format numbers in items_list
        for item in items_list:
            item['direction'] = _(item['direction'])
            item['f_budget'] = commas_format(item['budget'])
            item['f_actual'] = commas_format(item['actual'])

        context['items_list_json'] = renderer.render(items_list)

        # rendering initial state of breadcrumbs
        # setting initial scope name
        if scope_item:
            scope_item_serialized = SheetItemUISerializer(scope_item).data

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
                'actual': commas_format(reduce(lambda x, y: x + y['actual'], items_list, 0)),
                'budget': commas_format(reduce(lambda x, y: x + y['budget'], items_list, 0)),
                'direction': '',
                'code': ''
            }
            context['scope_name'] = _('Main')

        # rendering initial state of the items table
        context['items_list'] = render_to_string('items_list.ms', {
            'stache': items_list
        })
        return context
