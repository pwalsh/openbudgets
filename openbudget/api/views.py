from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from openbudget.api.serializers import GeoPoliticalEntitySerializer, BudgetTemplateSerializer, BudgetTemplateNodeSerializer, BudgetSerializer, BudgetItemSerializer, ActualSerializer, ActualItemSerializer
from openbudget.govts.models import GeoPoliticalEntity
from openbudget.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem


@api_view(['GET'])
def api_root(request, format=None):
    """The entry endpoint of our API"""

    return Response({
        'geopols': reverse('geopolitcalentity-list', request=request),
        'budgets': reverse('budget-list', request=request),
        'actuals': reverse('actual-list', request=request),
    })


class GeoPoliticalEntityList(generics.ListAPIView):
    """API endpoint that represents a list of geopols"""

    model = GeoPoliticalEntity
    serializer_class = GeoPoliticalEntitySerializer


class GeoPoliticalEntityDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single geopol"""

    model = GeoPoliticalEntity
    serializer_class = GeoPoliticalEntitySerializer


class BudgetTemplateDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget template"""

    model = BudgetTemplate
    serializer_class = BudgetTemplateSerializer


class BudgetTemplateNodeDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget template node"""

    model = BudgetTemplateNode
    serializer_class = BudgetTemplateNodeSerializer


class BudgetList(generics.ListAPIView):
    """API endpoint that represents a list of budgets"""

    model = Budget
    serializer_class = BudgetSerializer


class BudgetDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single budget"""

    model = Budget
    serializer_class = BudgetSerializer


class BudgetItemList(generics.ListAPIView):
    """API endpoint that represents a list of bitems"""

    model = BudgetItem
    serializer_class = BudgetItemSerializer


class BudgetItemDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single bitem"""

    model = BudgetItem
    serializer_class = BudgetItemSerializer


class ActualList(generics.ListAPIView):
    """API endpoint that represents a list of actuals"""

    model = Actual
    serializer_class = ActualSerializer


class ActualDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single actual"""

    model = Actual
    serializer_class = ActualSerializer


class ActualItemList(generics.ListAPIView):
    """API endpoint that represents a list of actual items"""

    model = ActualItem
    serializer_class = ActualItemSerializer


class ActualItemDetail(generics.RetrieveAPIView):
    """API endpoint that represents a single actual item"""

    model = ActualItem
    serializer_class = ActualItemSerializer
