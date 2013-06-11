import django_filters
from rest_framework import generics
from rest_framework.response import Response
from openbudget.apps.budgets.serializers import TemplateBaseSerializer, \
    TemplateNodeBaseSerializer, BudgetBaseSerializer, BudgetItemBaseSerializer,\
    ActualBaseSerializer, ActualItemBaseSerializer
from openbudget.apps.budgets.models import Template, TemplateNode, Budget, \
    BudgetItem, Actual, ActualItem


class TemplateList(generics.ListAPIView):
    """API endpoint that represents a list of budget templates"""

    model = Template
    serializer_class = TemplateBaseSerializer
    filter_fields = ('divisions', 'budgets', 'actuals')


class TemplateDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget template"""

    model = Template
    serializer_class = TemplateBaseSerializer


class TemplateNodeFilter(django_filters.FilterSet):

    class Meta:
        model = TemplateNode
        fields = ['templates']


class TemplateNodeList(generics.ListAPIView):
    """API endpoint that represents a list of template nodes"""

    model = TemplateNode
    serializer_class = TemplateNodeBaseSerializer
    filter_class = TemplateNodeFilter


class TemplateNodeDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget template node"""

    model = TemplateNode
    serializer_class = TemplateNodeBaseSerializer


class BudgetList(generics.ListAPIView):
    """API endpoint that represents a list of budgets"""

    model = Budget
    serializer_class = BudgetBaseSerializer


class BudgetDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget"""

    model = Budget
    serializer_class = BudgetBaseSerializer


class BudgetItemList(generics.ListAPIView):
    """API endpoint that represents a list of bitems"""

    model = BudgetItem
    serializer_class = BudgetItemBaseSerializer


class BudgetItemDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single bitem"""

    model = BudgetItem
    serializer_class = BudgetItemBaseSerializer


class ActualList(generics.ListAPIView):
    """API endpoint that represents a list of actuals"""

    model = Actual
    serializer_class = ActualBaseSerializer


class ActualDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single actual"""

    model = Actual
    serializer_class = ActualBaseSerializer


class ActualItemList(generics.ListAPIView):
    """API endpoint that represents a list of actual items"""

    model = ActualItem
    serializer_class = ActualItemBaseSerializer


class ActualItemDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single actual item"""

    model = ActualItem
    serializer_class = ActualItemBaseSerializer



class TemplateNodesListLatest(generics.ListAPIView):

    def get(self, request, entity_pk, *args, **kwargs):

        nodes = Template.objects.latest_of(entity=entity_pk).nodes
        serialized_nodes = TemplateNodeBaseSerializer(nodes, many=True).data

        return Response(serialized_nodes)


class NodeTimeline(generics.ListAPIView):
    """
    API endpoint that retrieves a timeline of budget items and actual items
    according to a given node, entity and optionally a period
    """

    def get(self, request, entity_pk, node_pk, *args, **kwargs):
        """GET handler for retrieving all budget items and actual items of the node's timeline, filtered by entity"""

        budget_items = BudgetItem.objects.timeline(node_pk, entity_pk)
        actual_items = ActualItem.objects.timeline(node_pk, entity_pk)

        budget_items_serialized = BudgetItemBaseSerializer(budget_items, many=True).data
        actual_items_serialized = ActualItemBaseSerializer(actual_items, many=True).data

        return Response({
            "budget_items": budget_items_serialized,
            "actual_items": actual_items_serialized
        })

