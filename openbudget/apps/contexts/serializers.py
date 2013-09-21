from rest_framework import serializers
from openbudget.apps.contexts import models


class ContextBaseSerializer(serializers.ModelSerializer):
    """Base Context serializer, exposing our defaults for contexts."""

    data = serializers.WritableField()

    class Meta:
        model = models.Context


class CoefficientBaseSerializer(serializers.HyperlinkedModelSerializer):
    """Base Coefficient serializer."""

    class Meta:
        model = models.Coefficient
