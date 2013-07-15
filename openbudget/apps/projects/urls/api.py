from django.conf.urls import patterns, url
from openbudget.apps.projects.views import api


urlpatterns = patterns('',

    url(r'^$',
        api.ProjectList.as_view(),
        name='project-list'
    ),
    url(r'^states/$',
        api.StateList.as_view(),
        name='state-list'
    ),
    url(
        r'^(?P<uuid>\w+)/$',
        api.ProjectDetail.as_view(),
        name='project-detail'
    ),
    url(
        r'^states/(?P<uuid>\w+)/$',
        api.StateDetail.as_view(),
        name='state-detail'
    ),
)
