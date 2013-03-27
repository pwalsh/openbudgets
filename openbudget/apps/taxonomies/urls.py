from django.conf.urls.defaults import patterns, url
from openbudget.apps.taxonomies.views import TaxonomyTagDetailView, TaxonomyDetailView


urlpatterns = patterns('',

    url(r'^(?P<slug>[-\w]+)/$',
        TaxonomyDetailView.as_view(),
        name='taxonomy_detail'
    ),

    url(r'^tag/(?P<slug>[-\w]+)/$',
        TaxonomyTagDetailView.as_view(),
        name='taxonomy_tag_detail'
    ),

)
