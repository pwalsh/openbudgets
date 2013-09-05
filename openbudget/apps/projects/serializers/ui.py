from rest_framework.fields import Field
from openbudget.apps.projects.serializers import api


class ProjectBase(api.ProjectBase):
    """Base Project serializer, exposing our defaults for projects."""

    url = Field(source='get_absolute_url')

    class Meta(api.ProjectBase.Meta):
        lookup_field = 'slug'
