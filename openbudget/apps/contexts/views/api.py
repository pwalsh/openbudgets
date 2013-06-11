from rest_framework.generics import ListAPIView, RetrieveAPIView
from openbudget.apps.contexts.serializers import ContextBaseSerializer
from openbudget.apps.contexts.models import Context
from openbudget.apps.contexts.filters import ContextFilter


class ContextList(ListAPIView):
    """Called via an API endpoint that represents a list of context objects."""

    model = Context
    queryset = Context.objects.related_map()
    serializer_class = ContextBaseSerializer
    filter_class = ContextFilter
    search_fields = ['data']


class ContextDetail(RetrieveAPIView):
    """Called via an API endpoint that represents a single context object."""

    model = Context
    queryset = Context.objects.related_map()
    serializer_class = ContextBaseSerializer
