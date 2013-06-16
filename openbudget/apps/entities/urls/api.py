from django.conf.urls import patterns, url
from openbudget.apps.entities.views import api


def entities():
    urlpatterns = patterns('',
        url(
            r'^$',
            api.EntityList.as_view(),
            name='entity-list'
        ),
        url(
            r'^(?P<pk>\d+)/$',
            api.EntityDetail.as_view(),
            name='entity-detail'
        ),
    )
    return urlpatterns


def divisions():
    urlpatterns = patterns('',
        url(
            r'^$',
            api.DivisionList.as_view(),
            name='division-list'
        ),
        url(
            r'^(?P<pk>\d+)/$',
            api.DivisionDetail.as_view(),
            name='division-detail'
        ),
    )
    return urlpatterns


def domains():
    urlpatterns = patterns('',
        url(
            r'^$',
            api.DomainList.as_view(),
            name='domain-list'
        ),
        url(
            r'^(?P<pk>\d+)/$',
            api.DomainDetail.as_view(),
            name='domain-detail'
        ),
    )
    return urlpatterns
