from rest_framework import serializers
from openbudget.apps.entities.models import Entity, Domain, DomainDivision
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.visualizations.models import Visualization


class BudgetTemplateNodeLinked(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BudgetTemplateNode


class UUIDField(serializers.RelatedField):
    def to_native(self, value):
        return str(value.uuid)

class BudgetTemplateNodeModel(serializers.ModelSerializer):

    backwards = UUIDField(many=True)
    forwards = UUIDField(many=True)
    inverse = UUIDField(many=True)

    class Meta:
        model = BudgetTemplateNode


class BudgetTemplateLinked(serializers.HyperlinkedModelSerializer):

    node_set = BudgetTemplateNodeModel()

    class Meta:
        model = BudgetTemplate


class PeriodField(serializers.RelatedField):
    def to_native(self, value):
        return {
            'period_start': value.period_start,
            'period_end': value.period_end
        }

class BudgetItemLinked(serializers.HyperlinkedModelSerializer):

    node = BudgetTemplateNodeModel()
    budget = PeriodField()

    class Meta:
        model = BudgetItem


class BudgetLinked(serializers.HyperlinkedModelSerializer):

    items = BudgetItemLinked()

    class Meta:
        model = Budget


class ActualItemLinked(serializers.HyperlinkedModelSerializer):

    node = BudgetTemplateNodeModel()
    actual = PeriodField()

    class Meta:
        model = ActualItem


class ActualLinked(serializers.HyperlinkedModelSerializer):

    items = ActualItemLinked()

    class Meta:
        model = Actual


class DomainDivisionBase(serializers.ModelSerializer):

    class Meta:
        model = DomainDivision

#TODO: changed from HyperlinkedModelSerializer to ModelSerializer to get the importer app working
class EntityListLinked(serializers.ModelSerializer):

    budgets = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='budget-detail')
    actuals = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='actual-detail')
    division = DomainDivisionBase()

    class Meta:
        model = Entity


class EntityDetailLinked(serializers.HyperlinkedModelSerializer):

    budgets = BudgetLinked()
    actuals = ActualLinked()

    class Meta:
        model = Entity


#TODO: changed from HyperlinkedModelSerializer to ModelSerializer to get the importer app working
class DomainDivisionLinked(DomainDivisionBase):

    entities = EntityListLinked()

    class Meta:
        model = DomainDivision


class DomainLinked(serializers.HyperlinkedModelSerializer):

    entities = EntityListLinked()
    divisions = DomainDivisionLinked()

    class Meta:
        model = Domain


class VisualizationLinked(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Visualization
