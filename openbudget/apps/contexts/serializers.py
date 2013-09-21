from rest_framework.serializers import HyperlinkedModelSerializer
from openbudget.apps.contexts import models


class ContextBaseSerializer(HyperlinkedModelSerializer):
    """Base Context serializer, exposing our defaults for contexts."""

    class Meta:
        model = models.Context


class CoefficientBaseSerializer(HyperlinkedModelSerializer):
    """Base Coefficient serializer."""

    class Meta:
        model = models.Coefficient
