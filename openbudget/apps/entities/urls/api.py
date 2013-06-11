from django.conf.urls import patterns, url
from openbudget.apps.entities.views.api import DomainList, DomainDetail,\
    DivisionList, DivisionDetail, EntityList, EntityDetail


urlpatterns = patterns('',

    url(r'^domains/$', DomainList.as_view(), name='domain-list'),

    url(r'^domains/(?P<pk>\d+)/$', DomainDetail.as_view(), name='domain-detail'),

    url(r'^divisions/$', DivisionList.as_view(), name='division-list'),

    url(r'^divisions/(?P<pk>\d+)/$', DivisionDetail.as_view(), name='division-detail'),

    url(r'^entities/$', EntityList.as_view(), name='entity-list'),

    url(r'^entities/(?P<pk>\d+)/$', EntityDetail.as_view(), name='entity-detail'),

)
