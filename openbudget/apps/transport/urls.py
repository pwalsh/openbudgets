from django.conf.urls import patterns, url
from openbudget.apps.transport.views import FileImportView


urlpatterns = patterns('',
    url(r'^import/$',
        FileImportView.as_view(),
        name='file_import'
    ),
)
