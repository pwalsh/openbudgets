from django.conf.urls import patterns, url
from openbudgets.apps.entities.views import api


def entities():

    urlpatterns = patterns('',
        url(r'^$',
            api.EntityList.as_view(), name='entity-list'),

        url(r'^(?P<pk>[-\w]+)/$',
            api.EntityDetail.as_view(), name='entity-detail'),
    )

    return urlpatterns


def divisions():

    urlpatterns = patterns('',
        url(r'^$',
            api.DivisionList.as_view(), name='division-list'),

        url(r'^(?P<pk>[-\w]+)/$',
            api.DivisionDetail.as_view(), name='division-detail'),
    )

    return urlpatterns


def domains():

    urlpatterns = patterns('',
        url(r'^$',
            api.DomainList.as_view(), name='domain-list'),

        url(r'^(?P<pk>[-\w]+)/$',
            api.DomainDetail.as_view(), name='domain-detail'),
    )

    return urlpatterns
