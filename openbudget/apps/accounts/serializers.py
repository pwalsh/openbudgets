from rest_framework.serializers import HyperlinkedModelSerializer, Field
from openbudget.apps.accounts import models


class AccountBaseSerializer(HyperlinkedModelSerializer):
    """Base Account serializer, exposing our defaults for accounts."""

    # url = Field(source='get_absolute_url')

    class Meta:
        model = models.Account
        fields = ['url', 'id', 'uuid', 'first_name', 'last_name', 'username',
                  'date_joined', 'email']
        lookup_field = 'uuid'
