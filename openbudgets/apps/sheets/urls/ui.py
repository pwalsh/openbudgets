from django.conf.urls import patterns, url
from openbudgets.apps.sheets.views import ui


urlpatterns = patterns('',
    url(
        r'^templates/$',
        ui.TemplateList.as_view(),
        name='template_list'
    ),
    url(
        r'^templates/(?P<pk>[-\w]+)/$',
        ui.TemplateDetail.as_view(),
        name='template_detail'
    ),
    url(
        r'^templates/nodes/(?P<pk>[-\w]+)/$',
        ui.TemplateNodeDetail.as_view(),
        name='template_node_detail'
    ),
    url(
        r'^sheets/$',
        ui.SheetList.as_view(),
        name='sheet_list'
    ),
    url(
        r'^sheets/items/(?P<pk>[-\w]+)/$',
        ui.SheetItemDetail.as_view(),
        name='sheet_item_detail'
    ),
    url(
        r'^sheets/(?P<entity_slug>[-\w]+)/(?P<period>[-\w]+)/$',
        ui.SheetDetail.as_view(),
        name='sheet_detail'
    ),
)
