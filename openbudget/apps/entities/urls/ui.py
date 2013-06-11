from django.conf.urls import patterns, url
from openbudget.apps.entities.views.ui import EntityDetail, EntityList


urlpatterns = patterns('',

    url(r'^$', EntityList.as_view(), name='entity_list'),

    url(r'^(?P<slug>[-\w]+)/$', EntityDetail.as_view(), name='entity_detail'),

)
