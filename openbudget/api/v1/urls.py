from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('openbudget.api.v1.views',

    url(r'^$', 'api_root', name='api_v1'),

    url(r'^auth/', include('provider.oauth2.urls', namespace='oauth2')),

    url(r'^entities/', include('openbudget.apps.entities.urls.api')),

    url(r'^budgets/', include('openbudget.apps.budgets.urls.api')),

    url(r'^contexts/', include('openbudget.apps.contexts.urls.api')),

    url(r'^projects/', include('openbudget.apps.projects.urls.api')),

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
