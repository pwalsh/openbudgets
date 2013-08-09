from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer, Field
from openbudget.apps.entities.models import Entity
from openbudget.apps.sheets.models import Sheet, SheetItem, TemplateNode
from openbudget.apps.international.utilities import translated_fields


class SheetItemUIMinSerializer(ModelSerializer):

    node = Field('node.id')
    code = Field('node.code')
    name = Field('node.name')
    name_en = Field('node.name_en')
    name_ar = Field('node.name_ar')
    name_ru = Field('node.name_ru')
    path = Field('node.path')
    direction = Field('node.direction')

    class Meta:
        model = SheetItem
        fields = ['id', 'uuid', 'code', 'name', 'path', 'direction', 'budget',
                  'actual', 'description', 'node']\
                 + translated_fields(TemplateNode)


class SheetItemUISerializer(ModelSerializer):

    node = Field('node.id')
    parent = SheetItemUIMinSerializer()
    children = SheetItemUIMinSerializer(many=True)
    ancestors = SheetItemUIMinSerializer(many=True)
    # descendants = SheetItemUIMinSerializer(many=True)
    code = Field('node.code')
    name = Field('node.name')
    name_en = Field('node.name_en')
    name_ar = Field('node.name_ar')
    name_ru = Field('node.name_ru')
    path = Field('node.path')
    direction = Field('node.direction')

    class Meta:
        model = SheetItem
        fields = ['id', 'uuid', 'code', 'name', 'path', 'direction', 'budget',
                  'actual', 'description', 'node', 'parent', 'children', 'ancestors', 'discussion']\
                 + translated_fields(TemplateNode)


class SheetUISerializer(ModelSerializer):

    period = Field(source='period')

    class Meta:
        model = Sheet
        fields = ['id', 'template', 'description', 'period'] + translated_fields(model)



class EntityDetailUISerializer(ModelSerializer):

    sheets = SheetUISerializer()

    class Meta:
        model = Entity
        fields = ['id', 'name', 'description', 'code', 'sheets', 'slug']\
                 + translated_fields(model)


class EntityList(ListView):
    model = Entity
    template_name = 'entities/entity_list.html'

    def get_context_data(self, **kwargs):

        context = super(EntityList, self).get_context_data(**kwargs)

        self.object_list = self.object_list.filter(division__index=3)
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
                    'period': s.period
                })



        context['sheets'] = sheets
        context['object_json'] = renderer.render(EntityDetailUISerializer(self.object).data)
        context['sheet_json'] = renderer.render(SheetUISerializer(sheet).data) if sheet else '{}'
        context['items_list_json'] = renderer.render(items_list)

        # rendering initial state of breadcrumbs
        # setting initial scope name
        if scope_item:
            scope_item_serialized = SheetItemUISerializer(scope_item).data
            context['scope_item_json'] = renderer.render(scope_item_serialized)
            context['items_breadcrumbs'] = render_to_string('items_breadcrumbs.ms', {
                'stache': scope_item_serialized['ancestors']
            })
            context['scope_name'] = scope_item_serialized['name']
        else:
            context['scope_item_json'] = '{}'
            context['items_breadcrumbs'] = ''
            context['scope_name'] = _('Main')

        # rendering initial state of the items table
        context['items_list'] = render_to_string('items_list.ms', {
            'stache': items_list
        })
        return context
