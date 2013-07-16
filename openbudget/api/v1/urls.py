from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from openbudget.apps.entities.urls.api import entities, divisions, domains
from openbudget.apps.sheets.urls.api import templates, sheets


urlpatterns = patterns('openbudget.api.v1.views',
    url(
        r'^$',
        'api_v1',
        name='api_v1'
    ),
    url(
        r'^entities/',
        include(entities())
    ),
    url(
        r'^divisions/',
        include(divisions())
    ),
    url(
        r'^domains/',
        include(domains())
    ),
    url(
        r'^templates/',
        include(templates())
    ),
    url(
        r'^sheets/',
        include(sheets())
    ),
    url(
        r'^contexts/',
        include('openbudget.apps.contexts.urls.api')
    ),
    url(
        r'^projects/',
        include('openbudget.apps.projects.urls.api')
    ),
    url(
        r'^accounts/',
        include('openbudget.apps.accounts.urls.api')
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
