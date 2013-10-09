from django.conf.urls import patterns, url
from openbudgets.apps.taxonomies.views import TagDetailView, TaxonomyDetailView


urlpatterns = patterns('',

    url(r'^(?P<slug>[-\w]+)/$',
        TaxonomyDetailView.as_view(), name='taxonomy_detail'),

    url(r'^tag/(?P<taxonomy_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        TagDetailView.as_view(), name='tag_detail'),

)
