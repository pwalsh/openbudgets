from rest_framework import serializers
from openbudget.entities.models import Entity, Domain, DomainDivision
from openbudget.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem


class BudgetTemplateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BudgetTemplate


class BudgetTemplateNodeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BudgetTemplateNode


class BudgetItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BudgetItem


class BudgetSerializer(serializers.HyperlinkedModelSerializer):

    items = BudgetItemSerializer()

    class Meta:
        model = Budget


class ActualItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ActualItem


class ActualSerializer(serializers.HyperlinkedModelSerializer):

    items = ActualItemSerializer()

    class Meta:
        model = Actual


class EntitySerializer(serializers.HyperlinkedModelSerializer):

    budgets = BudgetSerializer()

    class Meta:
        model = Entity


class DomainDivisionSerializer(serializers.HyperlinkedModelSerializer):

    entities = EntitySerializer()

    class Meta:
        model = DomainDivision


class DomainSerializer(serializers.HyperlinkedModelSerializer):

    entities = EntitySerializer()
    divisions = DomainDivisionSerializer()

    class Meta:
        model = Domain
