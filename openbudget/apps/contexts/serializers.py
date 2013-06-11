from rest_framework.serializers import HyperlinkedModelSerializer
from openbudget.apps.contexts.models import Context


class ContextBaseSerializer(HyperlinkedModelSerializer):
    """Base Context serializer, exposing our defaults for contexts."""

    class Meta:
        model = Context
