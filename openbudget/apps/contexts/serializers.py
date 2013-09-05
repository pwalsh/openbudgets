from rest_framework.serializers import ModelSerializer, WritableField
from openbudget.apps.contexts.models import Context


class ContextBaseSerializer(ModelSerializer):
    """Base Context serializer, exposing our defaults for contexts."""

    data = WritableField()

    class Meta:
        model = Context
