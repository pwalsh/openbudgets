from rest_framework import serializers
from openbudgets.apps.sheets import models
from openbudgets.apps.accounts.serializers import AccountMin
from openbudgets.commons.serializers import UUIDRelatedField, UUIDPrimaryKeyRelatedField
from openbudgets.apps.entities.serializers import EntityMin, DivisionMin


class TemplateMin(serializers.HyperlinkedModelSerializer):

    """Serializes Template objects for consumption by API.

    This minimal Template serializer is design for use as a nested object,
    in other serializers.

    """

    class Meta:
        model = models.Template
        fields = ['id', 'url']


class SheetMin(serializers.HyperlinkedModelSerializer):

    """Serializes Sheet objects for consumption by API.

    This minimal Sheet serializer is design for use as a nested object,
    in other serializers.

    """

    entity = EntityMin()
    period = serializers.Field(source='period')
    variance = serializers.Field('variance')

    class Meta:
        model = models.Sheet
        fields = ['id', 'url', 'entity', 'budget', 'actual', 'variance', 'period']


class TemplateNodeMin(serializers.HyperlinkedModelSerializer):

    """Serializes TemplateNode objects for consumption by API.

    This minimal TemplateNode serializer is design for use as a nested object,
    in other serializers.

    """

    class Meta:
        model = models.TemplateNode
        fields = ['id', 'url', 'name', 'code', 'path', 'comparable',
                  'depth', 'direction']


class SheetItemMin(serializers.HyperlinkedModelSerializer):

    """Serializes SheetItem objects for consumption by API.

    This minimal SheetItem serializer is design for use as a nested object, in other
    serializers.

    """

    node = serializers.Field(source='node_id')
    variance = serializers.Field(source='variance')

    class Meta:
        model = models.SheetItem
        fields = ['id', 'url', 'node', 'name', 'code', 'path', 'comparable',
                  'direction', 'depth', 'budget', 'actual', 'variance']


class Template(TemplateMin):

    """Serializes Template objects for consumption by API."""

    period = serializers.Field(source='period')
    blueprint = TemplateMin()
    is_blueprint = serializers.Field(source='is_blueprint')
    divisions = DivisionMin(many=True)
    sheets = SheetMin(many=True)
    has_sheets = serializers.Field(source='has_sheets')
    sheet_count = serializers.Field(source='sheet_count')
    nodes = TemplateNodeMin(many=True)
    node_count = serializers.Field(source='node_count')

    class Meta(TemplateMin.Meta):
        model = models.Template
        fields = TemplateMin.Meta.fields + ['name', 'description', 'period',
                 'blueprint', 'is_blueprint', 'divisions', 'sheets', 'has_sheets',
                 'sheet_count', 'nodes', 'node_count',  'created_on',
                 'last_modified']


class Sheet(SheetMin):

    """Serializes Sheet objects for consumption by API."""

    entity = EntityMin()
    template = TemplateMin()
    items = SheetItemMin(many=True)

    class Meta(SheetMin.Meta):
        fields = SheetMin.Meta.fields + ['entity', 'template', 'description',
                 'items', 'created_on', 'last_modified']


class TemplateNode(TemplateNodeMin):

    """Serializes TemplateNode objects for consumption by API."""

    templates = TemplateMin(many=True)
    parent = TemplateNodeMin()
    children = TemplateNodeMin(many=True)
    backwards = TemplateNodeMin(many=True)
    inverse = TemplateNodeMin(many=True)
    items = SheetItemMin(many=True)

    class Meta(TemplateNodeMin.Meta):
        fields = TemplateNodeMin.Meta.fields + ['code', 'name', 'description',
                 'direction', 'path', 'comparable', 'depth', 'templates',
                 'parent', 'children', 'backwards', 'inverse', 'items',
                 'created_on', 'last_modified']


class TemplateNodeAncestors(TemplateNode):

    """Serializes TemplateNode objects with ancestors field for consumption by API."""

    ancestors = TemplateNodeMin(many=True)

    class Meta(TemplateNode.Meta):
        fields = TemplateNode.Meta.fields + ['ancestors']


class SheetItem(SheetItemMin):

    """Serializes SheetItem objects for consumption by API."""

    parent = SheetItemMin()
    children = SheetItemMin(many=True)

    class Meta(SheetItemMin.Meta):
        fields = SheetItemMin.Meta.fields + ['sheet', 'depth', 'description',
                 'parent', 'children', 'has_comments', 'comment_count']


class SheetItemAncestors(SheetItem):

    """Serializes SheetItem objects for consumption by API."""

    ancestors = SheetItemMin(many=True)

    class Meta(SheetItem.Meta):
        fields = SheetItem.Meta.fields + ['ancestors']


class SheetTimeline(serializers.ModelSerializer):

    """Serializes SheetItem objects for consumption by API."""

    # TODO: Validate why we need this, why not just use the normal SheetItemMin serializer

    period = serializers.Field('period')

    class Meta:
        model = models.SheetItem
        fields = ['id', 'budget', 'actual', 'description', 'period']


class SheetItemCommentMin(serializers.HyperlinkedModelSerializer):

    """Serializes SheetItemComment objects for consumption by API."""

    user = UUIDRelatedField()
    item = UUIDPrimaryKeyRelatedField()

    class Meta:
        model = models.SheetItemComment
        fields = ['id', 'url', 'item', 'user', 'comment']


class SheetItemComment(SheetItemCommentMin):

    """Serializes SheetItemComment objects for consumption by API."""

    user = AccountMin()
    item = SheetItemMin()

    class Meta(SheetItemCommentMin.Meta):
        fields = SheetItemCommentMin.Meta.fields + ['created_on', 'last_modified']
