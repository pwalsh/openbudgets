from rest_framework import serializers
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.projects import models
from openbudget.apps.accounts.serializers import AccountMin
from openbudget.commons.serializers import UUIDRelatedField


class ProjectBaseSerializer(serializers.ModelSerializer):

    """Base Project serializer, exposing our defaults for projects."""

    author = AccountMin()
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = models.Project
        fields = ['id', 'url', 'author', 'label', 'name', 'description', 'featured',
                  'screenshot', 'created_on', 'last_modified'] +\
                 translated_fields(model)


class StateBaseSerializer(serializers.HyperlinkedModelSerializer):

    """Base State serializer, for creating new State instances
    and the base the serializer in charge of exposing our defaults for projects.

    """

    author = UUIDRelatedField()

    class Meta:
        model = models.State
        fields = ['id', 'url', 'project', 'author', 'screenshot', 'config',
                  'created_on', 'last_modified']


class StateReadSerializer(StateBaseSerializer):

    """Base State serializer, exposing our defaults for projects."""

    author = AccountMin()
