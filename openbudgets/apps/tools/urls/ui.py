from django.conf.urls import patterns, url
from openbudgets.apps.tools.views import ui


urlpatterns = patterns('',

    url(r'^$',
        ui.ToolListView.as_view(),
        name='tool_list'),

    url(r'^jsi18n/$',
        'django.views.i18n.javascript_catalog',
        {'packages': ('openbudgets.apps.tools',)},
        name='tools_js_i18n'),

    url(r'^embed/(?P<slug>[-\w]+)/(?P<state>[-\w]+)/$',
        ui.ToolEmbedView.as_view(),
        name='tool_embed'),

    url(r'^(?P<slug>[-\w]+)/(?P<id>[-\w]+)/$',
        ui.ToolDetailView.as_view(),
        name='state_detail'),

    url(r'^(?P<slug>[-\w]+)/$',
        ui.ToolDetailView.as_view(),
        name='tool_detail'),

)
