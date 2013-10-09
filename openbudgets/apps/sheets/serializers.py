from rest_framework import serializers
from openbudgets.apps.international.utilities import translated_fields
from openbudgets.apps.sheets import models
from openbudgets.apps.accounts.serializers import AccountMin
from openbudgets.commons.serializers import UUIDRelatedField
from openbudgets.apps.entities.serializers import EntityMin


class TemplateNodeMin(serializers.HyperlinkedModelSerializer):

    """Serializes TemplateNode objects for consumption by API.

    This minimal TemplateNode serializer is design for use as a nested object,
    in other serializers.

    """

    class Meta:
        model = models.TemplateNode
        fields = ['id', 'url']


class TemplateMin(serializers.HyperlinkedModelSerializer):

    """Serializes Template objects for consumption by API.

    This minimal Template serializer is design for use as a nested object, in other
    serializers.

    """

    period = serializers.Field(source='period')
    is_blueprint = serializers.Field(source='is_blueprint')
    has_sheets = serializers.Field(source='has_sheets')

    class Meta:
        model = models.Template
        fields = ['id', 'url', 'name', 'description', 'period', 'blueprint', 'is_blueprint',
                  'has_sheets']


class TemplateNode(TemplateNodeMin):

    """Serializes Template objects for consumption by API."""

    parent = TemplateNodeMin()
    backwards = TemplateNodeMin(many=True)
    inverse = TemplateNodeMin(many=True)

    class Meta(TemplateNodeMin.Meta):
        fields = TemplateNodeMin.Meta.fields + ['code', 'name', 'description',
                 'direction', 'path', 'comparable', 'parent', 'templates',
                 'backwards', 'inverse', 'items', 'created_on', 'last_modified',] \
                 + translated_fields(models.TemplateNode)


class Template(TemplateMin):

    """Serializes Template objects for consumption by API."""

    node_count = serializers.Field(source='node_count')
    nodes = TemplateNodeMin(many=True)

    class Meta(TemplateMin.Meta):
        fields = TemplateMin.Meta.fields + ['divisions', 'sheets', 'node_count', 'nodes', 'created_on',
                 'last_modified'] + translated_fields(models.Template)


class SheetItemMin(serializers.HyperlinkedModelSerializer):

    """Serializes SheetItem objects for consumption by API.

    This minimal SheetItem serializer is design for use as a nested object, in other
    serializers.

    """

    node = serializers.Field(source='node.pk')
    name = serializers.Field(source='name')
    code = serializers.Field(source='code')
    comparable = serializers.Field(source='comparable')
    direction = serializers.Field(source='direction')
    variance = serializers.Field(source='variance')
    path = serializers.Field(source='path')
    name_en = serializers.Field(source='node.name_en')
    name_ar = serializers.Field(source='node.name_ar')
    name_ru = serializers.Field(source='node.name_ru')

    class Meta:
        model = models.SheetItem
        fields = ['id', 'url', 'node', 'name', 'code', 'comparable', 'direction',
                  'path', 'budget', 'actual', 'variance'] + translated_fields(models.TemplateNode)


class SheetMin(serializers.HyperlinkedModelSerializer):

    """Serializes Sheet objects for consumption by API.

    This minimal Sheet serializer is design for use as a nested object, in other
    serializers.

    """

    period = serializers.Field(source='period')
    variance = serializers.Field('variance')

    class Meta:
        model = models.Sheet
        fields = ['id', 'url', 'budget', 'actual', 'variance', 'period']


class SheetItem(SheetItemMin):

    """Serializes SheetItem objects for consumption by API."""

    depth = serializers.Field(source='depth')
    has_comments = serializers.Field(source='has_comments')
    comment_count = serializers.Field(source='comment_count')
    parent = SheetItemMin()
    children = SheetItemMin(many=True)
    ancestors = SheetItemMin(many=True)
    name_en = serializers.Field('node.name_en')
    name_ar = serializers.Field('node.name_ar')
    name_ru = serializers.Field('node.name_ru')

    class Meta(SheetItemMin.Meta):
        fields = SheetItemMin.Meta.fields + ['sheet', 'depth', 'description',
                 'has_comments', 'comment_count', 'parent', 'children', 'ancestors',
                 'discussion'] + translated_fields(models.TemplateNode)


class Sheet(SheetMin):

    """Serializes Sheet objects for consumption by API."""

    entity = EntityMin()
    template = TemplateMin()

    class Meta(SheetMin.Meta):
        fields = SheetMin.Meta.fields + ['entity', 'template', 'description', 'items',
                 'created_on', 'last_modified'] + translated_fields(models.Sheet)


class SheetTimeline(serializers.ModelSerializer):

    """Serializes SheetItem objects for consumption by API."""

    # TODO: Validate why we need this, why not just use the normal SheetItemMin serializer

    period = serializers.Field('period')

    class Meta:
        model = models.SheetItem
        fields = ['id', 'budget', 'actual', 'description', 'period'] + translated_fields(model)


class SheetItemCommentEmbed(serializers.ModelSerializer):

    """Serializes SheetItemComment objects for consumption by API."""


    user = UUIDRelatedField()

    class Meta:
        model = models.SheetItemComment
        fields = ['comment', 'user']


class SheetItemCommentRead(SheetItemCommentEmbed):

    """Serializes SheetItemComment objects for consumption by API."""

    user = AccountMin()

    class Meta(SheetItemCommentEmbed.Meta):
        fields = SheetItemCommentEmbed.Meta.fields + \
                 ['id', 'item', 'created_on', 'last_modified']


class SheetItemCommentMin(serializers.HyperlinkedModelSerializer):

    """Serializes SheetItemComment objects for consumption by API.

    This minimal Sheet serializer is design for use as a nested object, in other
    serializers.

    """

    class Meta:
        model = models.SheetItemComment
        fields = ['id', 'url', 'comment', 'item', 'user']
