from rest_framework.serializers import HyperlinkedModelSerializer, \
    HyperlinkedRelatedField, Field
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.entities.models import Entity, Domain, Division
from openbudget.apps.budgets.serializers import BudgetNestedSerializer, \
    ActualNestedSerializer


class DomainBaseSerializer(HyperlinkedModelSerializer):
    """Base Domain serializer, exposing our defaults for domains."""

    divisions = HyperlinkedRelatedField(many=True, read_only=True, view_name='division-detail')

    class Meta:
        model = Domain
        fields = ['url', 'name', 'measurement_system', 'ground_surface_unit',
                  'currency', 'created_on', 'last_modified', 'divisions']\
                 + translated_fields('name')


class DomainDetailSerializer(DomainBaseSerializer):
    """Used to represent a full relational map of a domain."""
    # TODO: Make the below work
    # divisions = DivisionBaseSerializer()

    class Meta:
        model = Domain


class DomainNestedSerializer(DomainBaseSerializer):
    """Used to represent domains when nested in other objects."""

    class Meta(DomainBaseSerializer.Meta):
        fields = ('url', 'name')


class DivisionBaseSerializer(HyperlinkedModelSerializer):
    """Base Division serializer, exposing our defaults for divisions."""

    domain = DomainNestedSerializer()

    class Meta:
        model = Division
        fields = ['url', 'name', 'index', 'budgeting', 'domain', 'created_on',
                  'last_modified'] + translated_fields('name')


class DivisionDetailSerializer(DivisionBaseSerializer):
    """Used to represent a full relational map of a division."""

    domain = DomainNestedSerializer()
    entities = HyperlinkedRelatedField(many=True, read_only=True, view_name='entity-detail')


class DivisionNestedSerializer(DivisionBaseSerializer):
    """Used to represent divisions when nested in other objects."""

    domain = Field(source='domain')

    class Meta(DivisionBaseSerializer.Meta):
        fields = ('url', 'name', 'domain')


class EntityBaseSerializer(HyperlinkedModelSerializer):
    """Base Entity serializer, exposing our defaults for entities."""

    division = DivisionNestedSerializer()
    budgets = HyperlinkedRelatedField(many=True, read_only=True, view_name='budget-detail')
    actuals = HyperlinkedRelatedField(many=True, read_only=True, view_name='actual-detail')

    class Meta:
        model = Entity
        fields = ['url', 'name', 'description', 'code', 'parent', 'division',
                  'budgets', 'actuals', 'created_on','last_modified']\
                 + translated_fields('name')


class EntityDetailSerializer(EntityBaseSerializer):
    """Used to represent a full relational map of an entity."""

    budgets = BudgetNestedSerializer()
    actuals = ActualNestedSerializer()
