from django.conf.urls.defaults import patterns, url
from openbudget.apps.sources.views import AuxSourceDetailView, ReferenceSourceDetailView


urlpatterns = patterns('',

    url(r'^aux/(?P<slug>[-\w]+)/$',
        AuxSourceDetailView.as_view(),
        name='auxsource_detail'
    ),

    url(r'^reference/(?P<slug>[-\w]+)/$',
        ReferenceSourceDetailView.as_view(),
        name='referencesource_detail'
    ),

)
