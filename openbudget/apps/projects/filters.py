from django_filters import FilterSet
from openbudget.apps.projects.models import Project


class ProjectFilter(FilterSet):
    class Meta:
        model = Project
