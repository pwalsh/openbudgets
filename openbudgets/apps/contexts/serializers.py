from rest_framework import serializers
from openbudgets.apps.contexts import models
from openbudgets.apps.entities.serializers import EntityMin


class ContextBaseSerializer(serializers.HyperlinkedModelSerializer):
    """Base Context serializer, exposing our defaults for contexts."""

    data = serializers.WritableField()
    entity = EntityMin()

    class Meta:
        model = models.Context
        fields = ['id', 'url', 'entity', 'population', 'population_male',
                  'population_female', 'ground_surface', 'students', 'schools',
                  'gini_index', 'socioeconomic_index']


class CoefficientBaseSerializer(serializers.HyperlinkedModelSerializer):
    """Base Coefficient serializer."""

    class Meta:
        model = models.Coefficient
        fields = ['id', 'url', 'domain', 'inflation', 'period_start', 'period_end']
