from django.conf.urls import patterns, url
from openbudgets.apps.contexts.views import api


def contexts():

    urlpatterns = patterns('',
        url(r'^$',
            api.ContextList.as_view(), name='context-list'),

        url(r'^(?P<pk>[-\w]+)/$',
            api.ContextDetail.as_view(), name='context-detail'),
    )

    return urlpatterns


def coefficients():

    urlpatterns = patterns('',
        url(r'^$',
            api.CoefficientList.as_view(), name='coefficient-list'),

        url(r'^(?P<pk>[-\w]+)/$',
            api.CoefficientDetail.as_view(), name='coefficient-detail'),
    )

    return urlpatterns