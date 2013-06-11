from rest_framework.generics import ListAPIView, RetrieveAPIView
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.entities.serializers import DomainBaseSerializer,\
    DivisionBaseSerializer, DivisionDetailSerializer, EntityBaseSerializer,\
    EntityDetailSerializer
from openbudget.apps.entities.filters import DomainFilter, DivisionFilter,\
    EntityFilter
from openbudget.apps.entities.models import Entity, Domain, Division


class DomainList(ListAPIView):
    """Called via an API endpoint that represents a list of domain objects."""

    model = Domain
    queryset = Domain.objects.related_map()
    serializer_class = DomainBaseSerializer
    filter_class = DomainFilter
    search_fields = ['name'] + translated_fields('name')


class DomainDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single domain object."""

    model = Domain
    queryset = Domain.objects.related_map()
    serializer_class = DomainBaseSerializer


class DivisionList(ListAPIView):
    """Called via an API endpoint that represents a list of division objects."""

    model = Division
    queryset = Division.objects.related_map()
    serializer_class = DivisionBaseSerializer
    filter_class = DivisionFilter
    search_fields = ['name'] + translated_fields('name')


class DivisionDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single division object."""

    model = Division
    queryset = Division.objects.related_map()
    serializer_class = DivisionDetailSerializer


class EntityList(ListAPIView):
    """Called via an API endpoint that represents a list of entity objects."""

    model = Entity
    queryset = Entity.objects.related_map()
    serializer_class = EntityBaseSerializer
    filter_class = EntityFilter
    search_fields = ['name', 'description'] + translated_fields('name', 'description')


class EntityDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single entity object."""

    model = Entity
    queryset = Entity.objects.related_map()
    serializer_class = EntityDetailSerializer
