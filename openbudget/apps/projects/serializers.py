from rest_framework.serializers import HyperlinkedModelSerializer, RelatedField
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.projects.models import Project


class ProjectBaseSerializer(HyperlinkedModelSerializer):
    """Base Project serializer, exposing our defaults for projects."""

    owner = RelatedField()
    author = RelatedField()

    class Meta:
        model = Project
        fields = ['url', 'owner', 'author', 'name', 'description', 'featured',
                  'preview', 'created_on', 'last_modified'] +\
                 translated_fields(model)
