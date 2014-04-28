from rest_framework import serializers
from openbudgets.apps.tools import models
from openbudgets.apps.accounts.serializers import AccountMin
from openbudgets.commons.serializers import UUIDRelatedField, UUIDPrimaryKeyRelatedField


class Tool(serializers.HyperlinkedModelSerializer):
    """Base Project serializer, exposing our defaults for projects."""

    author = AccountMin()

    class Meta:
        model = models.Tool
        fields = ['id', 'slug', 'author', 'label', 'name', 'description',
                  'featured', 'screenshot', 'created_on', 'last_modified']


class State(serializers.HyperlinkedModelSerializer):
    """
    Base State serializer, for creating new State instances
    and the base the serializer in charge of exposing our defaults for projects.
    """

    author = UUIDRelatedField()
    tool = UUIDPrimaryKeyRelatedField()

    class Meta:
        model = models.State
        fields = ['url', 'id', 'tool', 'author', 'screenshot', 'config',
                  'created_on', 'last_modified']


class StateRead(State):
    """Base State serializer, exposing our defaults for projects."""

    author = AccountMin()
    config = serializers.WritableField()
