from rest_framework import serializers
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.sheets import models


class TemplateMin(serializers.HyperlinkedModelSerializer):
    """A minimal serializer for nested template objects."""

    class Meta:
        model = models.Template
        fields = ['id', 'url']


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


class SheetBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of sheets."""

    period = serializers.Field(source='period')
    # preventing circular import
    from openbudget.apps.entities.serializers import EntityMin
    entity = EntityMin()
    template = TemplateMin()

    class Meta:
        model = models.Sheet
        fields = ['id', 'url', 'template', 'entity', 'description', 'period',
                  'created_on', 'last_modified'] + translated_fields(model)


class SheetItemBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of sheet items."""

    node = TemplateNodeMin()

    class Meta:
        model = models.SheetItem
        fields = ['id', 'url', 'budget', 'actual', 'description', 'node',
                  'discussion'] + translated_fields(model)


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
