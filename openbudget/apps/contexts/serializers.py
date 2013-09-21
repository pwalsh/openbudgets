<<<<<<< HEAD
from rest_framework.serializers import HyperlinkedModelSerializer
from openbudget.apps.contexts import models
=======
from rest_framework.serializers import ModelSerializer, WritableField
from openbudget.apps.contexts.models import Context
>>>>>>> origin/develop


class ContextBaseSerializer(ModelSerializer):
    """Base Context serializer, exposing our defaults for contexts."""

    data = WritableField()

    class Meta:
        model = models.Context


class CoefficientBaseSerializer(HyperlinkedModelSerializer):
    """Base Coefficient serializer."""

    class Meta:
        model = models.Coefficient
