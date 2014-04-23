from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from openbudgets.api.v1.views import api_v1
from openbudgets.apps.entities.urls.api import entities, divisions, domains
from openbudgets.apps.sheets.urls.api import templates, sheets
from openbudgets.apps.contexts.urls.api import contexts, coefficients


urlpatterns = [

    url(r'^$', api_v1, name='api_v1'),

    url(r'^entities/', include(entities())),

    url(r'^divisions/', include(divisions())),

    url(r'^domains/', include(domains())),

    url(r'^templates/', include(templates())),

    url(r'^sheets/', include(sheets())),

    url(r'^contexts/', include(contexts())),

    url(r'^coefficients/', include(coefficients())),

    url(r'^tools/', include('openbudgets.apps.tools.urls.api')),

    url(r'^accounts/', include('openbudgets.apps.accounts.urls.api')),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
