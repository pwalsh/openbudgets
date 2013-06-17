from rest_framework import generics
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.entities import serializers
from openbudget.apps.entities import filters
from openbudget.apps.entities import models


class DomainList(generics.ListAPIView):
    """Called via an API endpoint that represents a list of domains."""

    model = models.Domain
    queryset = model.objects.related_map()
    serializer_class = serializers.DomainBase
    filter_class = filters.DomainFilter
    search_fields = ['name'] + translated_fields(model)


class DomainDetail(generics.RetrieveAPIView):
    """Called via an API endpoint that represents a single domain."""

    model = models.Domain
    queryset = model.objects.related_map()
    serializer_class = serializers.DomainDetail


class DivisionList(generics.ListAPIView):
    """Called via an API endpoint that represents a list of divisions."""

    model = models.Division
    queryset = model.objects.related_map()
    serializer_class = serializers.DivisionBase
    filter_class = filters.DivisionFilter
    search_fields = ['name'] + translated_fields(model)


class DivisionDetail(generics.RetrieveAPIView):
    """Called via an API endpoint that represents a single division."""

    model = models.Division
    queryset = model.objects.related_map()
    serializer_class = serializers.DivisionDetail


class EntityList(generics.ListAPIView):
    """Called via an API endpoint that represents a list of entities."""

    model = models.Entity
    #queryset = model.objects.related_map()
    serializer_class = serializers.EntityBase
    filter_class = filters.EntityFilter
    search_fields = ['name', 'description'] + translated_fields(model)

    def get_queryset(self):
        queryset = self.model.objects.related_map()
        budgeting = self.request.QUERY_PARAMS.get('budgeting', None)
        if budgeting:
            queryset = queryset.filter(division__budgeting=budgeting)
        return queryset

class EntityDetail(generics.RetrieveAPIView):
    """Called via an API endpoint that represents a single entity."""

    model = models.Entity
    queryset = model.objects.related_map()
    serializer_class = serializers.EntityDetail
