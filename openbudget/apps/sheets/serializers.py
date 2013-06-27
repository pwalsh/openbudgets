from rest_framework import serializers
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.sheets import models


class TemplateBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of templates."""

    period = serializers.Field(source='period')

    class Meta:
        model = models.Template
        fields = ['id', 'url', 'name', 'description', 'divisions', 'period',
                  'created_on', 'last_modified'] + translated_fields(model)


class TemplateNodeMin(serializers.HyperlinkedModelSerializer):
    """A more efficient serialized representation of template nodes."""

    class Meta:
        model = models.TemplateNode
        fields = ['id', 'url']


class TemplateNodeBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of template nodes."""

    parent = TemplateNodeMin()
    backwards = TemplateNodeMin(many=True)

    class Meta:
        model = models.TemplateNode
        fields = ['id', 'url', 'code', 'name', 'description', 'direction',
                  'templates', 'path', 'direction', 'parent', 'created_on',
                  'last_modified', 'backwards'] + translated_fields(model)


class TemplateDetail(TemplateBase):
    """A detailed, related representation of templates."""

    nodes = TemplateNodeBase()

    class Meta(TemplateBase.Meta):
        fields = TemplateBase.Meta.fields + ['nodes']


#TODO: change back to HyperlinkedModelSerializer once we fix the url of DenormalizedSheetItem
class SheetBase(serializers.ModelSerializer):
    """The default serialized representation of sheets."""

    period = serializers.Field(source='period')

    class Meta:
        model = models.Sheet
        #TODO: put 'url' back here once we fix the url of DenormalizedSheetItem
        fields = ['id', 'template', 'entity', 'description', 'period',
                  'created_on', 'last_modified'] + translated_fields(model)

#TODO: change back to HyperlinkedModelSerializer once we fix the url of DenormalizedSheetItem
class SheetItemBase(serializers.ModelSerializer):
    """The default serialized representation of sheet items."""

    url = serializers.HyperlinkedIdentityField(view_name='sheetitem-detail')
    node = TemplateNodeMin()

    class Meta:
        model = models.SheetItem
        #TODO: put 'url' back here once we fix the url of DenormalizedSheetItem
        fields = ['id', 'budget', 'actual', 'description', 'node'] + translated_fields(model)



class SheetDetail(SheetBase):
    """A detailed, related representation of sheets."""

    #entity = EntityBase()
    #total = serializers.DecimalField(source='total')
    items = SheetItemBase()

    class Meta(SheetBase.Meta):
        fields = SheetBase.Meta.fields + ['denormalizedsheetitems']


class SheetItemDetail(SheetItemBase):
    """A detailed, related representation of sheet items."""

    class Meta(SheetItemBase.Meta):
        fields = SheetItemBase.Meta.fields + ['discussion']


class SheetTimeline(serializers.ModelSerializer):

    period = serializers.SerializerMethodField('get_period')

    class Meta:
        model = models.SheetItem
        fields = ['id', 'budget', 'actual', 'description', 'period'] + translated_fields(model)

    def get_period(self, obj):
        return obj.sheet.period
