from django_filters import FilterSet
from openbudget.apps.projects.models import Project, State


class ProjectFilter(FilterSet):
    class Meta:
        model = Project


class StateFilter(FilterSet):
    class Meta:
        model = State
