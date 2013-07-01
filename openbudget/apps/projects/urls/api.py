from django.conf.urls import patterns, url
from openbudget.apps.projects.views import api


urlpatterns = patterns('',

    url(r'^$',
        api.ProjectList.as_view(),
        name='project-list'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        api.ProjectDetail.as_view(),
        name='project-detail'
    ),
    url(r'^states/$',
        api.StateList.as_view(),
        name='state-list'
    ),
    url(
        r'^states/(?P<pk>\d+)/$',
        api.StateDetail.as_view(),
        name='state-detail'
    ),
)
