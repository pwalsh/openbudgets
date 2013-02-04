from django.conf.urls import patterns, url
from omuni.govts.views import GeoPolDetailView, GeoPolListView


urlpatterns = patterns('',

    url(r'^$',
        GeoPolListView.as_view(),
        name='geopol_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        GeoPolDetailView.as_view(),
        name='geopol_detail'
    ),

)
