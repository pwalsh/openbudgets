from django.conf.urls import patterns, url
from openbudgets.apps.sources.views import AuxSourceDetailView, ReferenceSourceDetailView


urlpatterns = patterns('',

    url(r'^aux/(?P<pk>[-\w]+)/$',
        AuxSourceDetailView.as_view(), name='auxsource_detail'),

    url(r'^reference/(?P<pk>[-\w]+)/$',
        ReferenceSourceDetailView.as_view(), name='referencesource_detail'),

)
