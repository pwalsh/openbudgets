from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_v1(request):
    """The entry endpoint of our v1 API"""

    return Response({
        # TODO: Absolutely must be private! This endpoint exposes user data!
        'Accounts': reverse('account-list', request=request),

        'Domains': reverse('domain-list', request=request),
        'Divisions': reverse('division-list', request=request),
        'Entities': reverse('entity-list', request=request),
        'Templates': reverse('template-list', request=request),

        # Shouldn't be publicly declared, it is an implementation detail.
        # The same data can be better retrieved from the sheet items endpoint.
        'Template Nodes': reverse('templatenode-list', request=request),
        'Sheets': reverse('sheet-list', request=request),
        'Sheet Items': reverse('sheetitem-list', request=request),
        'Sheet Item Comments': reverse('sheetitemcomment-list', request=request),
        #'Sheet Item Timeline': reverse('sheetitem-timeline', request=request),
        'Contexts': reverse('context-list', request=request),
        'Coefficients': reverse('coefficient-list', request=request),
        'Tools': reverse('tool-list', request=request),
        'Tool States': reverse('state-list', request=request),
    })
