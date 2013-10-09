from rest_framework import generics
from openbudgets.apps.accounts import serializers
from openbudgets.apps.accounts import models


class AccountList(generics.ListAPIView):

    """Called via an API endpoint that represents a list of account objects."""

    model = models.Account
    queryset = model.objects.all()
    serializer_class = serializers.AccountBaseSerializer
    ordering = ['last_name', 'first_name', 'username', 'email', 'date_joined']
    search_fields = ['last_name', 'first_name', 'username', 'email']


class AccountDetail(generics.RetrieveAPIView):

    """Called via an API endpoint that represents a single account object."""

    model = models.Account
    serializer_class = serializers.AccountBaseSerializer
