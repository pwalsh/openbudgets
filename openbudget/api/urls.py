from django.conf.urls import patterns, include, url
from openbudget.api.views import api_index


urlpatterns = patterns('',

    url(r'^$',
        api_index,
        name='api'
    ),
    url(r'^auth/',
        include('oauth2_provider.urls')
    ),
    url(r'^v1/',
        include('openbudget.api.v1.urls'),
    ),

)
