from rest_framework import generics
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.projects import serializers
from openbudget.apps.projects import models


class ProjectList(generics.ListAPIView):
    """Called via an API endpoint that represents a list of project objects."""

    model = models.Project
    queryset = model.objects.related_map()
    serializer_class = serializers.ProjectBaseSerializer
    ordering = ['id', 'created_on', 'last_modified']
    search_fields = ['name', 'description', 'owner__first_name',
                     'owner__last_name', 'author__first_name',
                     'author__first_name',] + translated_fields(model)


class ProjectDetail(generics.RetrieveAPIView):
    """Called via an API endpoint that represents a single project object."""

    model = models.Project
    queryset = model.objects.related_map()
    lookup_field = 'uuid'
    serializer_class = serializers.ProjectBaseSerializer


class StateList(generics.ListCreateAPIView):
    """Called via an API endpoint that represents a list of state objects."""

    model = models.State
    queryset = model.objects.related_map()
    search_fields = ['author__first_name', 'author__last_name', 'project__name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # base serializer for creating States
            return serializers.StateBaseSerializer
        # State list/retrieve serializer
        return serializers.StateReadSerializer


class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    """Called via an API endpoint that represents a single state object."""

    model = models.State
    queryset = model.objects.related_map()
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            # State list/retrieve serializer
            return serializers.StateReadSerializer
        # base serializer for creating States
        return serializers.StateBaseSerializer
