from rest_framework import generics
from rest_framework.response import Response
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.budgets import serializers
from openbudget.apps.budgets import models
from openbudget.apps.budgets import filters


class TemplateList(generics.ListAPIView):
    """API endpoint that represents a list of templates."""

    model = models.Template
    queryset = model.objects.related_map_min()
    serializer_class = serializers.TemplateBase
    filter_class = filters.TemplateFilter
    ordering = ['period_start']
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
    serializer_class = serializers.TemplateNodeMin
    filter_class = filters.TemplateNodeFilter
    search_fields = ['name', 'description'] + translated_fields(model)


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
    ordering = ['period_start']
    search_fields = ['entity__name', 'description', 'period_start',
                     'period_end'] + translated_fields(model)


class SheetDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget."""

    model = models.Sheet
    queryset = model.objects.related_map()
    serializer_class = serializers.SheetDetail


class SheetItemList(generics.ListAPIView):
    """API endpoint that represents a list of budget items."""

    model = models.SheetItem
    queryset = model.objects.related_map_min()
    serializer_class = serializers.SheetItemBase
    filter_class = filters.SheetItemFilter
    search_fields = ['sheet__entity__name', 'node__code', 'node__name',
                     'node__description', 'description', 'period_start',
                     'period_end'] + translated_fields(model) + \
                    translated_fields(models.TemplateNode)


class SheetItemDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget item."""

    model = models.SheetItem
    queryset = model.objects.related_map()
    serializer_class = serializers.SheetItemBase


class TemplateNodesListLatest(generics.ListAPIView):

    def get(self, request, entity_pk, *args, **kwargs):

        nodes = models.Template.objects.latest_of(entity=entity_pk).nodes
        serialized_nodes = serializers.TemplateNodeBase(nodes, many=True).data

        return Response(serialized_nodes)


class NodeTimeline(generics.ListAPIView):
    """
    API endpoint that retrieves a timeline of budget items and actual items
    according to a given node, entity and optionally a period
    """

    def get(self, request, entity_pk, node_pk, *args, **kwargs):
        """GET handler for retrieving all budget items and actual items of the node's timeline, filtered by entity"""

        budget_items = models.BudgetItem.objects.timeline(node_pk, entity_pk)
        actual_items = models.ActualItem.objects.timeline(node_pk, entity_pk)

        budget_items_serialized = serializers.BudgetItemBase(budget_items, many=True).data
        actual_items_serialized = serializers.ActualItemBase(actual_items, many=True).data

        return Response({
            "budget_items": budget_items_serialized,
            "actual_items": actual_items_serialized
        })
