from django.conf.urls import patterns, url
from openbudget.apps.projects.views.ui import ProjectListView, ProjectDetailView, ProjectView


urlpatterns = patterns('',

    url(r'^$',
        ProjectListView.as_view(),
        name='project_list'
    ),

    url(r'^jsi18n/$',
        'django.views.i18n.javascript_catalog',
        {'packages': ('openbudget.apps.projects',)},
        name='projects_js_i18n'
    ),

    url(r'^ext/(?P<slug>[-\w]+)/',
        ProjectView.as_view(),
        name='project_view'
    ),

    url(r'^(?P<slug>[-\w]+)/$',
        ProjectDetailView.as_view(),
        name='project_detail'
    ),

)
