from rest_framework import serializers
from openbudget.apps.entities.models import Entity, Domain, DomainDivision
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem


class BudgetTemplateLinked(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BudgetTemplate


class BudgetTemplateNodeLinked(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BudgetTemplateNode


class BudgetTemplateNodeModel(serializers.ModelSerializer):

    class Meta:
        model = BudgetTemplateNode


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


class EntityLinked(serializers.HyperlinkedModelSerializer):

    budgets = BudgetLinked()
    actuals = ActualLinked()

    class Meta:
        model = Entity


class DomainDivisionLinked(serializers.HyperlinkedModelSerializer):

    entities = EntityLinked()

    class Meta:
        model = DomainDivision


class DomainLinked(serializers.HyperlinkedModelSerializer):

    entities = EntityLinked()
    divisions = DomainDivisionLinked()

    class Meta:
        model = Domain
