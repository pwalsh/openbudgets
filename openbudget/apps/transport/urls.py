from django.conf.urls import patterns, url
from openbudget.apps.transport.views import DataImportView, ImportSuccessView, DataExportView


urlpatterns = patterns('',
    url(r'^import/$',
        DataImportView.as_view(),
        name='data_import'
    ),
    url(r'^import/success/$',
        ImportSuccessView.as_view(),
        name='import_success'
    ),
    url(r'^export/(?P<model>[\w-]+)/(?P<uuid>[\w-]+)/(?P<format>[\w-]+)/$',
        DataExportView.as_view(),
        name='data_export'
    ),
)
