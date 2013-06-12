from django_filters import FilterSet
from openbudget.apps.entities.models import Entity, Domain, Division


class DomainFilter(FilterSet):
    class Meta:
        model = Domain


class DivisionFilter(FilterSet):
    class Meta:
        model = Division
        fields = ('budgeting', 'index')


class EntityFilter(FilterSet):
    class Meta:
        model = Entity
        fields = ('division__budgeting', 'parent')
