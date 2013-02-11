from rest_framework import serializers
from omuni.govts.models import GeoPoliticalEntity
from omuni.budgets.models import Budget, BudgetItem


class BudgetItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BudgetItem


class BudgetSerializer(serializers.HyperlinkedModelSerializer):

    items = BudgetItemSerializer()

    class Meta:
        model = Budget
        fields = ('uuid', 'geopol', 'period_start', 'period_end', 'description', 'items')


class GeoPoliticalEntitySerializer(serializers.HyperlinkedModelSerializer):

    budgets = BudgetSerializer()

    class Meta:
        model = GeoPoliticalEntity
        fields = ('name', 'code', 'type_is', 'parent', 'budgets')
