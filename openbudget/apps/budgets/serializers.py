from rest_framework import serializers
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.budgets import models


class TemplateBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of templates."""

    period = serializers.Field(source='period')

    class Meta:
        model = models.Template
        fields = ['id', 'url', 'name', 'description', 'divisions', 'period',
                  'created_on', 'last_modified'] + translated_fields(model)


class TemplateNodeBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of template nodes."""

    class Meta:
        model = models.TemplateNode
        fields = ['id', 'url', 'code', 'name', 'description', 'direction',
                  'templates', 'direction', 'parent', 'created_on',
                  'last_modified'] + translated_fields(model)


class TemplateNodeMin(TemplateNodeBase):
    """A more efficient serialized representation of template nodes."""

    class Meta(TemplateNodeBase.Meta):
        fields = TemplateNodeBase.Meta.fields.remove('templates')


class BudgetBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of budgets."""

    period = serializers.Field(source='period')

    class Meta:
        model = models.Budget
        fields = ['id', 'url', 'entity', 'description', 'period',
                  'created_on', 'last_modified'] + translated_fields(model)


class BudgetItemBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of budget items."""

    class Meta:
        model = models.BudgetItem
        fields = ['id', 'url', 'node', 'amount', 'description', 'created_on',
                  'last_modified'] + translated_fields(model)


class ActualBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of budgets."""

    period = serializers.Field(source='period')

    class Meta:
        model = models.Actual
        fields = ['id', 'url', 'entity', 'description', 'period', 'created_on',
                  'last_modified'] + translated_fields(model)


class ActualItemBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of actuals items."""

    class Meta:
        model = models.ActualItem
        fields = ['id', 'url', 'node', 'amount', 'description', 'created_on',
                  'last_modified'] + translated_fields(model)


class TemplateDetail(TemplateBase):
    """A detailed, related representation of templates."""

    nodes = TemplateNodeBase()

    class Meta(TemplateBase.Meta):
        fields = TemplateBase.Meta.fields + ['nodes']


class BudgetDetail(BudgetBase):
    """A detailed, related representation of budgets."""

    #entity = EntityBase()
    #total = serializers.DecimalField(source='total')
    items = BudgetItemBase()

    class Meta(BudgetBase.Meta):
        fields = BudgetBase.Meta.fields + ['items']


class BudgetItemDetail(BudgetBase):
    """A detailed, related representation of budget items."""

    class Meta(BudgetItemBase.Meta):
        fields = BudgetItemBase.Meta.fields + ['discussion']


class ActualDetail(BudgetBase):
    """A detailed, related representation of actuals."""

    #entity = EntityBase
    #total = serializers.DecimalField(source='total')
    #items = ActualItemBase()

    class Meta(ActualBase.Meta):
        fields = ActualBase.Meta.fields + ['items']


class ActualItemDetail(BudgetBase):
    """A detailed, related representation of actuals items."""

    class Meta(ActualItemBase.Meta):
        fields = ActualItemBase.Meta.fields + ['discussion']
