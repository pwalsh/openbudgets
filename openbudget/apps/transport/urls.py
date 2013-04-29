from django.conf.urls import patterns, url
from openbudget.apps.transport.views import FileImportView, ImportSuccessView, FileExportView, importer_app


urlpatterns = patterns('',
    url(r'^import/$',
        FileImportView.as_view(),
        name='data_import'
    ),
    url(r'^import/success/$',
        ImportSuccessView.as_view(),
        name='import_success'
    ),
    url(r'^export/(?P<model>[\w-]+)/(?P<uuid>[\w-]+)/(?P<format>[\w-]+)/$',
        FileExportView.as_view(),
        name='data_export'
    ),
    url(r'^importer/$',
        importer_app,
        name='importer_app'
    ),
)
