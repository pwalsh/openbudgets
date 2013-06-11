from django_filters import FilterSet
from openbudget.apps.contexts.models import Context


class ContextFilter(FilterSet):
    class Meta:
        model = Context
