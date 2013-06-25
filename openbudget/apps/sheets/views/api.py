from rest_framework import generics
from rest_framework.response import Response
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.sheets import serializers
from openbudget.apps.sheets import models
from openbudget.apps.sheets import filters


class TemplateList(generics.ListAPIView):
    """API endpoint that represents a list of templates."""

    model = models.Template
    queryset = model.objects.related_map_min()
    serializer_class = serializers.TemplateBase
    filter_class = filters.TemplateFilter
    ordering = ['name', 'period_start', 'created_on', 'last_modified']
    search_fields = ['name', 'description'] + translated_fields(model)


class TemplateDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single template."""

    model = models.Template
    queryset = model.objects.related_map()
    serializer_class = serializers.TemplateDetail


class TemplateNodeList(generics.ListAPIView):
    """API endpoint that represents a list of template nodes."""

    model = models.TemplateNode
    queryset = model.objects.related_map_min()
    serializer_class = serializers.TemplateNodeBase
    filter_class = filters.TemplateNodeFilter
    ordering = ['name', 'created_on', 'last_modified']
    search_fields = ['name', 'description'] + translated_fields(model)

    def get_queryset(self):
        queryset = self.model.objects.all()
        entity = self.request.QUERY_PARAMS.get('entity', None)
        latest = self.request.QUERY_PARAMS.get('latest', None)
        if entity is not None:
            if latest:
                queryset = models.Template.objects.latest_of(entity=entity).nodes
            else:
                pass
        return queryset


class TemplateNodeDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single template node."""

    model = models.TemplateNode
    queryset = model.objects.related_map()
    serializer_class = serializers.TemplateNodeBase


class SheetList(generics.ListAPIView):
    """API endpoint that represents a list of budget sheets."""

    model = models.Sheet
    queryset = model.objects.related_map_min()
    serializer_class = serializers.SheetBase
    filter_class = filters.SheetFilter
    ordering = ['entity__name', 'period_start', 'created_on', 'last_modified']
    search_fields = ['entity__name', 'description', 'period_start',
                     'period_end'] + translated_fields(model)


class SheetDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget."""

    model = models.Sheet
    queryset = model.objects.related_map()
    serializer_class = serializers.SheetDetail


class SheetItemList(generics.ListAPIView):
    """API endpoint that represents a list of budget items."""

    model = models.DenormalizedSheetItem
    queryset = model.objects.related_map_min()
    serializer_class = serializers.SheetItemBase
    filter_class = filters.SheetItemFilter
    ordering = ['sheet__entity__name', 'code']
    search_fields = ['sheet__entity__name', 'code', 'name',
                     'node_description', 'description', 'period_start',
                     'period_end'] + translated_fields(model)

    def get_queryset(self):
        queryset = self.model.objects.all()
        entity = self.request.QUERY_PARAMS.get('entity', None)
        latest = self.request.QUERY_PARAMS.get('latest', None)
        if entity is not None:
            if latest:
                queryset = models.Sheet.objects.latest_of(entity=entity).denormalizedsheetitems
            else:
                pass
        return queryset


class SheetItemDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget item."""

    model = models.DenormalizedSheetItem
    queryset = model.objects.related_map()
    serializer_class = serializers.SheetItemBase


class TemplateNodesListLatest(generics.ListAPIView):

    def get(self, request, entity_pk, *args, **kwargs):

        nodes = models.Template.objects.latest_of(entity=entity_pk).nodes
        serialized_nodes = serializers.TemplateNodeBase(nodes, many=True).data

        return Response(serialized_nodes)


class ItemsTimeline(generics.ListAPIView):
    """
    API endpoint that retrieves a timeline of budget items and actual items
    according to a given node, entity and optionally a period
    """

    def get(self, request, entity_pk, node_pk, *args, **kwargs):
        """GET handler for retrieving all budget items and actual items of the node's timeline, filtered by entity"""

        items = models.SheetItem.objects.timeline(node_pk, entity_pk)

        serialized_timeline = serializers.SheetTimeline(items, many=True).data

        return Response(serialized_timeline)
