from rest_framework import serializers
from rest_framework.fields import get_component
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.comments.models import Comment
from openbudget.apps.entities.models import Entity, Domain, Division
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.projects.models import Project


class TemplateNodeLinked(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BudgetTemplateNode


class UUIDField(serializers.RelatedField):
    def to_native(self, value):
        return str(value.uuid)

class TemplateNodeModel(serializers.ModelSerializer):

    backwards = UUIDField(many=True)
    forwards = UUIDField(many=True)
    inverse = UUIDField(many=True)

    class Meta:
        model = BudgetTemplateNode


class TemplateLinked(serializers.HyperlinkedModelSerializer):

    node_set = TemplateNodeModel()

    class Meta:
        model = BudgetTemplate


class PeriodField(serializers.RelatedField):
    def to_native(self, value):
        return {
            'period_start': value.period_start,
            'period_end': value.period_end
        }


class CommentField(serializers.RelatedField):

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


class BudgetItemLinked(serializers.HyperlinkedModelSerializer):

    node = TemplateNodeModel()
    budget = PeriodField()

    class Meta:
        model = BudgetItem


class BudgetLinked(serializers.HyperlinkedModelSerializer):

    items = BudgetItemLinked()

    class Meta:
        model = Budget


class ActualItemLinked(serializers.HyperlinkedModelSerializer):

    node = TemplateNodeModel()
    actual = PeriodField()
    discussion = CommentField(many=True)

    class Meta:
        model = ActualItem


class ActualLinked(serializers.HyperlinkedModelSerializer):

    items = ActualItemLinked()

    class Meta:
        model = Actual


class DivisionBase(serializers.ModelSerializer):

    class Meta:
        model = Division

#TODO: changed from HyperlinkedModelSerializer to ModelSerializer to get the importer app working
class EntityListLinked(serializers.ModelSerializer):

    budgets = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='budget-detail')
    actuals = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='actual-detail')
    division = DivisionBase()

    class Meta:
        model = Entity


class EntityDetailLinked(serializers.HyperlinkedModelSerializer):

    budgets = BudgetLinked()
    actuals = ActualLinked()

    class Meta:
        model = Entity


#TODO: changed from HyperlinkedModelSerializer to ModelSerializer to get the importer app working
class DivisionLinked(DivisionBase):

    entities = EntityListLinked()

    class Meta:
        model = Division


class DomainLinked(serializers.HyperlinkedModelSerializer):

    entities = EntityListLinked()
    divisions = DivisionLinked()

    class Meta:
        model = Domain


class ProjectLinked(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
