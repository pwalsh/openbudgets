from rest_framework import serializers
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.sheets import models
from openbudget.apps.sheets.serializers import SheetItemCommentReadSerializer


class SheetTimeline(serializers.ModelSerializer):

    period = serializers.SerializerMethodField('get_period')

    class Meta:
        model = models.SheetItem
        fields = ['id', 'budget', 'actual', 'description', 'period'] + translated_fields(model)

    def get_period(self, obj):
        return obj.sheet.period


class SheetItemUIMinSerializer(serializers.ModelSerializer):

    node = serializers.Field('node.id')
    code = serializers.Field('node.code')
    name = serializers.Field('node.name')
    name_en = serializers.Field('node.name_en')
    name_ar = serializers.Field('node.name_ar')
    name_ru = serializers.Field('node.name_ru')
    path = serializers.Field('node.path')
    direction = serializers.Field('node.direction')

    class Meta:
        model = models.SheetItem
        fields = ['id', 'code', 'name', 'path', 'direction', 'budget',
                  'actual', 'description', 'node']\
                 + translated_fields(models.TemplateNode)


class SheetItemUISerializer(serializers.ModelSerializer):

    node = serializers.Field('node.id')
    parent = SheetItemUIMinSerializer()
    children = SheetItemUIMinSerializer(many=True)
    ancestors = SheetItemUIMinSerializer(many=True)
    # descendants = SheetItemUIMinSerializer(many=True)
    code = serializers.Field('node.code')
    name = serializers.Field('node.name')
    name_en = serializers.Field('node.name_en')
    name_ar = serializers.Field('node.name_ar')
    name_ru = serializers.Field('node.name_ru')
    path = serializers.Field('node.path')
    direction = serializers.Field('node.direction')
    has_comments = serializers.SerializerMethodField('get_has_comments')
    comments_count = serializers.SerializerMethodField('get_comments_count')
    discussion = SheetItemCommentReadSerializer(many=True)

    class Meta:
        model = models.SheetItem
        fields = ['id', 'code', 'name', 'path', 'direction', 'budget', 'actual',
                  'description', 'discussion', 'has_comments', 'comments_count',
                  'node', 'parent', 'children', 'ancestors']\
                 + translated_fields(models.TemplateNode)

    def get_has_comments(self, obj):
        if len(obj.description):
            return True
        return obj.discussion.exists()

    def get_comments_count(self, obj):
        count = 0
        if len(obj.description):
            count = 1
        count += obj.discussion.count()
        return count


class SheetUISerializer(serializers.ModelSerializer):

    period = serializers.Field(source='period')

    class Meta:
        model = models.Sheet
        fields = ['id', 'template', 'description', 'period'] + translated_fields(model)
