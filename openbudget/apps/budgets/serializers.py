from rest_framework.serializers import HyperlinkedModelSerializer, \
    HyperlinkedRelatedField, RelatedField, Field, DecimalField, IntegerField
from rest_framework.fields import get_component
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.comments.models import Comment
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.budgets.models import Template, TemplateNode, Budget, \
    BudgetItem, Actual, ActualItem


class TemplateBaseSerializer(HyperlinkedModelSerializer):
    """Base Domain serializer, exposing our defaults for templates."""

    divisions = HyperlinkedRelatedField(many=True, read_only=True, view_name='division-detail')

    class Meta:
        model = Template
        fields = ['url', 'name', 'description', 'divisions', 'period_start',
                  'created_on','last_modified']\
                 + translated_fields('name', 'description')


class TemplateDetailSerializer(TemplateBaseSerializer):
    """Used to represent a full relational map of a template."""

    class Meta:
        model = Template


class TemplateNodeBaseSerializer(HyperlinkedModelSerializer):
    """."""

    #divisions = HyperlinkedRelatedField(many=True, read_only=True, view_name='division-detail')

    class Meta:
        model = TemplateNode


class BudgetBaseSerializer(HyperlinkedModelSerializer):
    """Base Budget serializer, exposing our defaults for budgets."""

    period = Field(source='period')
    total = DecimalField(source='total')
    item_count = IntegerField(source='item_count')

    class Meta:
        model = Budget
        fields = ['url', 'entity', 'template', 'description', 'period',
                  'total', 'item_count', 'created_on', 'last_modified']\
                 + translated_fields('description')


class BudgetNestedSerializer(BudgetBaseSerializer):
    """Used to represent divisions when nested in other objects."""

    class Meta(BudgetBaseSerializer.Meta):
        fields = ('url', 'description', 'period', 'total', 'item_count')


class BudgetItemBaseSerializer(HyperlinkedModelSerializer):
    """Base BudgetItem serializer, exposing our defaults for budget items."""

    class Meta:
        model = BudgetItem


class ActualBaseSerializer(HyperlinkedModelSerializer):
    """Base Actual serializer, exposing our defaults for actuals."""

    period = Field(source='period')
    total = DecimalField(source='total')
    item_count = IntegerField(source='item_count')
    variance = DecimalField(source='variance')

    class Meta:
        model = Actual
        fields = ['url', 'entity', 'template', 'description', 'period',
                  'total', 'item_count', 'variance', 'created_on',
                  'last_modified'] + translated_fields('description')


class ActualNestedSerializer(ActualBaseSerializer):
    """Used to represent divisions when nested in other objects."""

    class Meta(ActualBaseSerializer.Meta):
        fields = ('url', 'description', 'period', 'total', 'item_count',
                  'variance')


class ActualItemBaseSerializer(HyperlinkedModelSerializer):
    """Base ActualItem serializer, exposing our defaults for actual items."""

    class Meta:
        model = ActualItem


class BudgetItemLinked(HyperlinkedModelSerializer):

    #node = TemplateNodeModel()
    #budget = PeriodField()

    class Meta:
        model = BudgetItem


class BudgetLinked(HyperlinkedModelSerializer):

    class Meta:
        model = Budget


class ActualItemLinked(HyperlinkedModelSerializer):

    #node = TemplateNodeModel()
    #actual = PeriodField()
    #discussion = CommentField(many=True)

    class Meta:
        model = ActualItem


class ActualLinked(HyperlinkedModelSerializer):

    #items = ActualItemLinked()

    class Meta:
        model = Actual



class TemplateNodeLinked(HyperlinkedModelSerializer):

    class Meta:
        model = TemplateNode



class CommentField(RelatedField):

    many = True

    def to_native(self, value):
        """."""
        return {'comment': value.comment}

    def field_to_native(self, obj, field_name):
        try:
            if self.source == '*':
                return self.to_native(obj)

            source = self.source or field_name
            value = obj

            for component in source.split('.'):
                value = get_component(value, component)
                if value is None:
                    break
        except ObjectDoesNotExist:
            return None

        if value is None:
            return None

        if self.many:
            return [self.to_native(item) for item in value.all()]
        return self.to_native(value)

    class Meta:
        model = Comment


