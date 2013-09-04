from django.conf.urls import patterns, url
from openbudget.apps.contexts.views import api


urlpatterns = patterns('',
    url(r'^$',
        api.ContextList.as_view(), name='context-list'),

    url(r'^(?P<pk>\d+)/$',
        api.ContextDetail.as_view(), name='context-detail'),

)
