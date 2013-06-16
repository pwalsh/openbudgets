from django.conf.urls import patterns, url
from openbudget.apps.budgets.views import ui


urlpatterns = patterns('',
    url(
        r'^templates/$',
        ui.TemplateList.as_view(),
        name='template_list'
    ),
    url(
        r'^templates/(?P<slug>[-\w]+)/$',
        ui.TemplateDetail.as_view(),
        name='template_detail'
    ),
    url(
        r'^sheets/$',
        ui.SheetList.as_view(),
        name='sheet_list'
    ),
    url(
        r'^sheets/(?P<entity_slug>[-\w]+)/(?P<period>[-\w]+)/$',
        ui.SheetDetail.as_view(),
        name='sheet_detail'
    ),
    url(
        r'^sheets/items/(?P<slug>[-\w]+)/$',
        ui.SheetItemDetail.as_view(),
        name='sheet_item_detail'
    ),
)
