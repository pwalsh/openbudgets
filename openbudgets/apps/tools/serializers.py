from rest_framework import serializers
from openbudgets.apps.international.utilities import translated_fields
from openbudgets.apps.tools import models
from openbudgets.apps.accounts.serializers import AccountMin
from openbudgets.commons.serializers import UUIDRelatedField, UUIDPKRelatedField


class Tool(serializers.HyperlinkedModelSerializer):
    """Base Project serializer, exposing our defaults for projects."""

    author = AccountMin()

    class Meta:
        model = models.Tool
        fields = ['url', 'id', 'author', 'label', 'name', 'description', 'featured',
                  'screenshot', 'created_on', 'last_modified'] +\
                  translated_fields(model)


class State(serializers.HyperlinkedModelSerializer):
    """
    Base State serializer, for creating new State instances
    and the base the serializer in charge of exposing our defaults for projects.
    """

    author = UUIDRelatedField()
    tool = UUIDPKRelatedField()

    class Meta:
        model = models.State
        fields = ['url', 'id', 'tool', 'author', 'screenshot', 'config',
                  'created_on', 'last_modified']


class StateRead(State):
    """Base State serializer, exposing our defaults for projects."""

    author = AccountMin()
    config = serializers.WritableField()
