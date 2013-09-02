from rest_framework.serializers import ModelSerializer
from openbudget.apps.contexts.models import Context


class ContextBaseSerializer(ModelSerializer):
    """Base Context serializer, exposing our defaults for contexts."""

    class Meta:
        model = Context
