from django.conf.urls import patterns, url
from openbudgets.apps.tools.views import ui


urlpatterns = patterns('',

    url(r'^$',
        ui.ToolListView.as_view(),
        name='project_list'),

    url(r'^jsi18n/$',
        'django.views.i18n.javascript_catalog',
        {'packages': ('openbudget.apps.tools',)},
        name='tools_js_i18n'),

    url(r'^(?P<slug>[-\w]+)/',
        ui.ToolDetailView.as_view(),
        name='tool_detail'),

)
