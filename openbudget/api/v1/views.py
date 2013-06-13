from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """The entry endpoint of our API"""

    return Response({
        'domains': reverse('domain-list', request=request),
        'divisions': reverse('division-list', request=request),
        'entities': reverse('entity-list', request=request),
        'templates': reverse('template-list', request=request),
        'templates/nodes': reverse('templatenode-list', request=request),
        'budgets': reverse('budget-list', request=request),
        'budgets/items/': reverse('budgetitem-list', request=request),
        'actuals': reverse('actual-list', request=request),
        'actuals/items': reverse('actualitem-list', request=request),
        'contexts': reverse('context-list', request=request),
        'projects': reverse('project-list', request=request),
    })
