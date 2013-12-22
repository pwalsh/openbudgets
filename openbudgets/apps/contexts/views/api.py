import datetime
from rest_framework.generics import ListAPIView, RetrieveAPIView
from openbudgets.apps.contexts import serializers
from openbudgets.apps.contexts import models


class ContextList(ListAPIView):
    """Called via an API endpoint that represents a list of context objects."""

    model = models.Context
    queryset = model.objects.related_map()
    serializer_class = serializers.ContextBaseSerializer
    ordering = ['id', 'entity__name', 'period_start', 'created_on', 'last_modified']
    search_fields = ['entity__name']

    def get_queryset(self):
        queryset = super(ContextList, self).get_queryset()

        ### FILTERS
        domains = self.request.QUERY_PARAMS.get('domains', None)
        divisions = self.request.QUERY_PARAMS.get('divisions', None)
        entities = self.request.QUERY_PARAMS.get('entities', None)
        periods = self.request.QUERY_PARAMS.get('periods', None)
        get_latest = self.request.QUERY_PARAMS.get('get_latest', None)

        # DOMAINS: return contexts used in the given domain(s).
        if domains:
            domains = domains.split(',')
            queryset = queryset.filter(entity__division__domain__in=domains)

        # DIVISIONS: return contexts used in the given division(s).
        if divisions:
            divisions = divisions.split(',')
            queryset = queryset.filter(entity__divisions__in=divisions)

        # ENTITIES: return contexts used by the given entity(-ies).
        if entities:
            entities = entities.split(',')
            queryset = queryset.filter(entity__in=entities)

        # PERIODS: return contexts matching the given period(s).
        if periods:
            periods = [datetime.date(int(p), 1, 1) for p in periods.split(',')]
            queryset = queryset.filter(period_start__in=periods)

        return queryset


class ContextDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single context object."""

    model = models.Context
    queryset = model.objects.related_map()
    serializer_class = serializers.ContextBaseSerializer


class CoefficientList(ListAPIView):
    """Called via an API endpoint that represents a list of coefficient objects."""

    model = models.Coefficient
    queryset = model.objects.all()
    serializer_class = serializers.CoefficientBaseSerializer
    ordering = ['domain', 'inflation']
    search_fields = ['domain__name']

    def get_queryset(self):
        queryset = super(CoefficientList, self).get_queryset()

        ### FILTERS
        domains = self.request.QUERY_PARAMS.get('domains', None)

        # DOMAINS: return contexts used in the given domain(s).
        if domains:
            domains = domains.split(',')
            queryset = queryset.filter(entity__division__domain__in=domains)

        return queryset


class CoefficientDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single coefficient object."""

    model = models.Coefficient
    queryset = model.objects.all()
    serializer_class = serializers.CoefficientBaseSerializer
