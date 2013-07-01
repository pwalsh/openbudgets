from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_v1(request):
    """The entry endpoint of our v1 API"""

    return Response({
        'Domains': reverse('domain-list', request=request),
        'Divisions': reverse('division-list', request=request),
        'Entities': reverse('entity-list', request=request),
        'Templates': reverse('template-list', request=request),
        'Template Nodes': reverse('templatenode-list', request=request),
        'Sheets': reverse('sheet-list', request=request),
        'Sheet Items': reverse('sheetitem-list', request=request),
        #'Sheet Item Timeline': reverse('sheetitem-timeline', request=request),
        'Contexts': reverse('context-list', request=request),
        'Projects': reverse('project-list', request=request),
        'Project States': reverse('state-list', request=request),
    })
