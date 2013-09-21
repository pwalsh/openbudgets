from rest_framework import serializers
from openbudget.apps.accounts.serializers import AccountMin
from openbudget.apps.projects.serializers import api
from openbudget.apps.projects import models


class ProjectBase(api.ProjectBase):
    """Base Project serializer, exposing our defaults for projects."""

    url = serializers.Field(source='get_absolute_url')

    class Meta(api.ProjectBase.Meta):
        lookup_field = 'slug'


class StateBase(serializers.ModelSerializer):

    """
    Base State serializer, for creating new State instances
    and the base the serializer in charge of exposing our defaults for projects.
    """

    author = AccountMin()
    config = serializers.WritableField()
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = models.State
        fields = ['url', 'uuid', 'project', 'author', 'screenshot', 'config',
                  'created_on', 'last_modified']
        lookup_field = 'uuid'

