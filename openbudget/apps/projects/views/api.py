from rest_framework.generics import ListAPIView, RetrieveAPIView
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.projects.serializers import ProjectBaseSerializer
from openbudget.apps.projects.models import Project
from openbudget.apps.projects.filters import ProjectFilter


class ProjectList(ListAPIView):
    """Called via an API endpoint that represents a list of project objects."""

    model = Project
    queryset = Project.objects.related_map()
    serializer_class = ProjectBaseSerializer
    filter_class = ProjectFilter
    search_fields = ['name', 'description', 'owner', 'author']\
                    + translated_fields(model)


class ProjectDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single project object."""

    model = Project
    queryset = Project.objects.related_map()
    serializer_class = ProjectBaseSerializer
