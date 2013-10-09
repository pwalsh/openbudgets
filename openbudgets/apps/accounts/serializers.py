from rest_framework import serializers
from openbudgets.apps.accounts import models


class AccountBaseSerializer(serializers.HyperlinkedModelSerializer):

    """Base Account serializer, exposing our defaults for accounts."""

    class Meta:
        model = models.Account
        fields = ['url', 'uuid', 'first_name', 'last_name', 'date_joined', 'email']


class AccountMin(serializers.ModelSerializer):

    """A minimal serializer for use as a nested entity representation."""

    avatar = serializers.Field(source='avatar')

    class Meta:
        model = models.Account
        fields = ['uuid', 'first_name', 'last_name', 'avatar']
