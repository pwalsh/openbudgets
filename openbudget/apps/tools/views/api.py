from rest_framework import generics
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.tools import serializers
from openbudget.apps.tools import models
from openbudget.apps.accounts.models import Account


class ToolList(generics.ListAPIView):
    """Called via an API endpoint that represents a list of tool objects."""

    model = models.Tool
    queryset = model.objects.related_map()
    serializer_class = serializers.ToolBaseSerializer
    ordering = ['id', 'created_on', 'last_modified']
    search_fields = ['name', 'description', 'owner__first_name',
                     'owner__last_name', 'author__first_name',
                     'author__first_name',] + translated_fields(model)


class ToolDetail(generics.RetrieveAPIView):
    """Called via an API endpoint that represents a single tool object."""

    model = models.Tool
    queryset = model.objects.related_map()
    serializer_class = serializers.ToolBaseSerializer


class StateListCreate(generics.ListCreateAPIView):
    """Called via an API endpoint that represents a list of state objects."""

    model = models.State
    queryset = model.objects.related_map()
    search_fields = ['author__first_name', 'author__last_name', 'tool__name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # base serializer for creating States
            return serializers.StateBase
        # State list/retrieve serializer
        return serializers.StateRead

    def pre_save(self, obj):
        obj.author = Account.objects.get(uuid=self.request.DATA.get('author'))
        obj.tool = models.Tool.objects.get(uuid=self.request.DATA.get('tool'))


class StateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Called via an API endpoint that represents a single state object."""

    model = models.State
    queryset = model.objects.related_map()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            # State list/retrieve serializer
            return serializers.StateRead
        # base serializer for creating States
        return serializers.StateBase
