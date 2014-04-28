from rest_framework import serializers
from openbudgets.apps.entities import models


class EntityMin(serializers.HyperlinkedModelSerializer):

    """A minimal serializer for use as a nested entity representation."""

    class Meta:
        model = models.Entity
        fields = ['id', 'url']


class DivisionMin(serializers.HyperlinkedModelSerializer):

    """A minimal serializer for use as a nested division representation."""

    class Meta:
        model = models.Division
        fields = ['id', 'url']


class EntityBase(serializers.HyperlinkedModelSerializer):

    """The default serialized representation of entities."""

    def __init__(self, *args, **kwargs):
        super(EntityBase, self).__init__(*args, **kwargs)
        from openbudgets.apps.sheets.serializers import SheetMin
        self.fields['sheets'] = SheetMin(many=True)

    parent = EntityMin()
    division = DivisionMin()

    class Meta:
        model = models.Entity
        fields = ['id', 'url', 'name', 'description', 'code', 'parent',
                  'division', 'created_on', 'last_modified']


class DivisionBase(serializers.HyperlinkedModelSerializer):

    """The default serialized representation of divisions."""

    entity_count = serializers.Field(source='entity_count')

    class Meta:
        model = models.Division
        fields = ['id', 'url', 'name', 'index', 'budgeting', 'domain',
                  'created_on', 'last_modified', 'entity_count']


class DomainBase(serializers.HyperlinkedModelSerializer):

    """The default serialized representation of domains."""

    class Meta:
        model = models.Domain
        fields = ['id', 'url', 'name', 'measurement_system',
                  'ground_surface_unit', 'currency', 'created_on',
                  'last_modified', 'divisions']


class DomainDetail(DomainBase):

    """A detailed, related representation of domain."""

    divisions = DivisionBase()


class DivisionDetail(DivisionBase):

    """Used to represent a full relational map of a division."""

    domain = DomainBase()
    # don't show self again on nested objects
    del domain.fields['divisions']

    class Meta(DivisionBase.Meta):
        fields = DivisionBase.Meta.fields + ['entities']


class EntityDetail(EntityBase):

    """A detailed, related representation of entities."""
    # preventing circular import
    #from openbudget.apps.sheets.serializers import Sheet
    #sheets = Sheet()
