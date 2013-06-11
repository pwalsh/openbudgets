from django.conf.urls import patterns, url
from openbudget.apps.projects.views.api import ProjectList, ProjectDetail


urlpatterns = patterns('',

    url(r'^projects/$', ProjectList.as_view(), name='project-list'),

    url(r'^projects/(?P<pk>\d+)/$', ProjectDetail.as_view(),
        name='project-detail'),

)
