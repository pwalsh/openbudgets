from rest_framework import serializers
from openbudgets.apps.contexts import models


class ContextBaseSerializer(serializers.HyperlinkedModelSerializer):
    """Base Context serializer, exposing our defaults for contexts."""

    data = serializers.WritableField()

    class Meta:
        model = models.Context
        fields = ['id', 'url', 'entity', 'data']


class CoefficientBaseSerializer(serializers.HyperlinkedModelSerializer):
    """Base Coefficient serializer."""

    class Meta:
        model = models.Coefficient
        fields = ['id', 'url', 'domain', 'inflation']
