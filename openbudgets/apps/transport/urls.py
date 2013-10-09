from django.conf.urls import patterns, url
from openbudgets.apps.transport.views import FileImportView, ImportSuccessView, \
    FileExportView, ImportAppView


urlpatterns = patterns('',

    url(r'^import/$',
        FileImportView.as_view(), name='data_import'),

    url(r'^import/success/$',
        ImportSuccessView.as_view(), name='import_success'),

    url(r'^export/(?P<model>[\w-]+)/(?P<pk>[\w-]+)/(?P<format>[\w-]+)/$',
        FileExportView.as_view(), name='data_export'),

    url(r'^importer/$',
        ImportAppView.as_view(), name='importer_app'),

    url(r'^jsi18n/$',
        'django.views.i18n.javascript_catalog',
        {'packages': ('openbudget.apps.transport',)}),

)
