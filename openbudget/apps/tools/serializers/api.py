from rest_framework.reverse import reverse
from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField, WritableField
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.projects import models
from openbudget.apps.accounts.serializers import AccountMin
from openbudget.commons.serializers import UUIDRelatedField


class ProjectBase(HyperlinkedModelSerializer):
    """Base Project serializer, exposing our defaults for projects."""

    author = AccountMin()
    url = SerializerMethodField('get_api_url')

    class Meta:
        model = models.Project
        fields = ['url', 'uuid', 'author', 'label', 'name', 'description', 'featured',
                  'screenshot', 'created_on', 'last_modified'] +\
                 translated_fields(model)
        lookup_field = 'uuid'

    def get_api_url(self, obj):
        return reverse('project-detail', args=[str(obj.uuid)])


class StateBase(HyperlinkedModelSerializer):
    """
    Base State serializer, for creating new State instances
    and the base the serializer in charge of exposing our defaults for projects.
    """

    author = UUIDRelatedField()
    project = UUIDRelatedField()
    url = SerializerMethodField('get_api_url')

    class Meta:
        model = models.State
        fields = ['url', 'uuid', 'project', 'author', 'screenshot', 'config',
                  'created_on', 'last_modified']
        lookup_field = 'uuid'

    def get_api_url(self, obj):
        return reverse('state-detail', args=[str(obj.uuid)])


class StateRead(StateBase):
    """Base State serializer, exposing our defaults for projects."""

    author = AccountMin()
    config = WritableField()
