from rest_framework.generics import ListAPIView, RetrieveAPIView
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.projects import serializers
from openbudget.apps.projects import models
from openbudget.apps.projects import filters


class ProjectList(ListAPIView):
    """Called via an API endpoint that represents a list of project objects."""

    model = models.Project
    queryset = model.objects.related_map()
    serializer_class = serializers.ProjectBaseSerializer
    filter_class = filters.ProjectFilter
    search_fields = ['name', 'description', 'owner', 'author']\
                    + translated_fields(model)


class ProjectDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single project object."""

    model = models.Project
    queryset = model.objects.related_map()
    serializer_class = serializers.ProjectBaseSerializer


class StateList(ListAPIView):
    """Called via an API endpoint that represents a list of state objects."""

    model = models.State
    queryset = model.objects.related_map()
    serializer_class = serializers.StateBaseSerializer
    filter_class = filters.StateFilter
    search_fields = ['author__first_name', 'author__last_name', 'project__name']


class StateDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single state object."""

    model = models.State
    queryset = model.objects.related_map()
    serializer_class = serializers.StateBaseSerializer
