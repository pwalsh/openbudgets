from rest_framework import serializers
from openbudget.govts.models import GeoPoliticalEntity
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


class GeoPoliticalEntitySerializer(serializers.HyperlinkedModelSerializer):

    budgets = BudgetSerializer()

    class Meta:
        model = GeoPoliticalEntity
