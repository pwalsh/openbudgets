from django.conf.urls import patterns, url
from openbudget.apps.transport.views import FileImportView, ImportSuccessView


urlpatterns = patterns('',
    url(r'^import/$',
        FileImportView.as_view(),
        name='file_import'
    ),
    url(r'^import/success/$',
        ImportSuccessView.as_view(),
        name='import_success'
    ),
)
