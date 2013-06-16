from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_index(request):
    """API Index"""

    return Response({'v1': reverse('api_v1', request=request)})
