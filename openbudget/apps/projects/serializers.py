from rest_framework.serializers import HyperlinkedModelSerializer, RelatedField
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.projects import models


class ProjectBaseSerializer(HyperlinkedModelSerializer):
    """Base Project serializer, exposing our defaults for projects."""

    owner = RelatedField()
    author = RelatedField()

    class Meta:
        model = models.Project
        fields = ['url', 'id', 'owner', 'author', 'name', 'description', 'featured',
                  'preview', 'created_on', 'last_modified'] +\
                 translated_fields(model)


class StateBaseSerializer(HyperlinkedModelSerializer):
    """Base State serializer, exposing our defaults for projects."""

    #project = RelatedField()
    #author = RelatedField()

    class Meta:
        model = models.State
        fields = ['url', 'id', 'project', 'author', 'preview', 'config',
                  'created_on', 'last_modified']
