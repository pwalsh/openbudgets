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

    model = models.Budget
    queryset = model.objects.related_map_min()
    serializer_class = serializers.BudgetBase
    filter_class = filters.BudgetFilter
    ordering = ['period_start']
    search_fields = ['entity__name', 'description', 'period_start',
                     'period_end'] + translated_fields(model)


class SheetDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget."""

    model = models.Budget
    queryset = model.objects.related_map()
    serializer_class = serializers.BudgetDetail


class SheetItemList(generics.ListAPIView):
    """API endpoint that represents a list of budget items."""

    model = models.BudgetItem
    queryset = model.objects.related_map_min()
    serializer_class = serializers.BudgetItemBase
    filter_class = filters.BudgetItemFilter
    search_fields = ['budget__entity__name', 'node__code', 'node__name',
                     'node__description', 'description', 'period_start',
                     'period_end'] + translated_fields(model) + \
                    translated_fields(models.TemplateNode)


class SheetItemDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget item."""

    model = models.BudgetItem
    queryset = model.objects.related_map()
    serializer_class = serializers.BudgetItemBase


class ActualList(generics.ListAPIView):
    """API endpoint that represents a list of actuals sheets."""

    model = models.Actual
    queryset = model.objects.related_map_min()
    serializer_class = serializers.ActualBase
    filter_class = filters.ActualFilter
    ordering = ['period_start']
    search_fields = ['entity__name', 'description', 'period_start',
                     'period_end'] + translated_fields(model)


class ActualDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single actuals sheet."""

    model = models.Actual
    queryset = model.objects.related_map()
    serializer_class = serializers.ActualDetail


class ActualItemList(generics.ListAPIView):
    """API endpoint that represents a list of actual items"""

    model = models.ActualItem
    queryset = model.objects.related_map_min()
    serializer_class = serializers.ActualItemBase
    filter_class = filters.ActualItemFilter
    search_fields = ['actual__entity__name', 'node__code', 'node__name',
                     'node__description', 'description', 'period_start',
                     'period_end'] + translated_fields(model) + \
                    translated_fields(models.TemplateNode)


class ActualItemDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single actuals item."""

    model = models.ActualItem
    queryset = model.objects.related_map()
    serializer_class = serializers.ActualItemBase


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
