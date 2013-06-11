from django.conf.urls import patterns, url
from openbudget.apps.projects.views.ui import ProjectListView, ProjectDetailView


urlpatterns = patterns('',

    url(r'^$',
        ProjectListView.as_view(),
        name='project_list'
    ),

    url(r'^(?P<slug>[-\w]+)/$',
        ProjectDetailView.as_view(),
        name='project_detail'
    ),

)
