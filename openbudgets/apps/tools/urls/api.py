from django.conf.urls import patterns, url
from openbudgets.apps.tools.views import api


urlpatterns = patterns('',

    url(r'^$',
        api.ToolList.as_view(), name='tool-list'),

    url(r'^states/$',
        api.StateListCreate.as_view(), name='state-list'),

    url(
        r'^(?P<pk>\w+)/$',
        api.ToolDetail.as_view(), name='tool-detail'),

    url(
        r'^states/(?P<pk>\w+)/$',
        api.StateRetrieveUpdateDestroy.as_view(), name='state-detail'),

)
