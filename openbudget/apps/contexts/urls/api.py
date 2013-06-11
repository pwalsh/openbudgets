from django.conf.urls import patterns, url
from openbudget.apps.contexts.views.api import ContextList, ContextDetail


urlpatterns = patterns('',

    url(r'^contexts/$', ContextList.as_view(), name='context-list'),

    url(r'^contexts/(?P<pk>\d+)/$', ContextDetail.as_view(),
        name='context-detail'),

)
