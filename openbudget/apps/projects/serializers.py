from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, Field, RelatedField
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.projects import models
from openbudget.apps.accounts.serializers import AccountMin


class ProjectBaseSerializer(ModelSerializer):
    """Base Project serializer, exposing our defaults for projects."""

    author = AccountMin()
    url = Field(source='get_absolute_url')

    class Meta:
        model = models.Project
        fields = ['url', 'uuid', 'author', 'label', 'description', 'featured',
                  'screenshot', 'created_on', 'last_modified'] +\
                 translated_fields(model)
        lookup_field = 'uuid'


class StateBaseSerializer(ModelSerializer):
    """
    Base State serializer, for creating new State instances
    and the base the serializer in charge of exposing our defaults for projects.
    """

    url = Field(source='get_absolute_url')

    class Meta:
        model = models.State
        fields = ['url', 'uuid', 'id', 'project', 'author', 'preview', 'config',
                  'created_on', 'last_modified']


class StateReadSerializer(StateBaseSerializer):
    """Base State serializer, exposing our defaults for projects."""

    author = AccountMin()
