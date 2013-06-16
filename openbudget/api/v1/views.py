from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_v1(request):
    """The entry endpoint of our v1 API"""

    return Response({
        'domains': reverse('domain-list', request=request),
        'divisions': reverse('division-list', request=request),
        'entities': reverse('entity-list', request=request),
        'templates': reverse('template-list', request=request),
        'templates/nodes': reverse('templatenode-list', request=request),
        'sheets': reverse('sheet-list', request=request),
        'sheets/items/': reverse('sheetitem-list', request=request),
        'contexts': reverse('context-list', request=request),
        'projects': reverse('project-list', request=request),
    })
