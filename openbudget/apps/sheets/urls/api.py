from django.conf.urls import patterns, url
from openbudget.apps.sheets.views import api


def templates():
    urlpatterns = patterns('',
        url(
            r'^$',
            api.TemplateList.as_view(),
            name='template-list'
        ),
        url(
            r'^(?P<pk>\d+)/$',
            api.TemplateDetail.as_view(),
            name='template-detail'
        ),
        url(
            r'^nodes/$',
            api.TemplateNodeList.as_view(),
            name='templatenode-list'
        ),
        url(
            r'^nodes/(?P<pk>\d+)/$',
            api.TemplateNodeDetail.as_view(),
            name='templatenode-detail'
        ),
        url(
            r'^nodes/latest/(?P<entity_pk>\w+)/$',
            api.TemplateNodesListLatest.as_view(),
            name='node-list-latest'
        ),
    )
    return urlpatterns


def sheets():
    urlpatterns = patterns('',
        url(
            r'^$',
            api.SheetList.as_view(),
            name='sheet-list'
        ),
        url(
            r'^(?P<pk>\d+)/$',
            api.SheetDetail.as_view(),
            name='sheet-detail'
        ),
        url(
            r'^items/$',
            api.SheetItemList.as_view(),
            name='sheetitem-list'
        ),
        url(
            r'^items/(?P<pk>\d+)/$',
            api.SheetItemDetail.as_view(),
            name='sheetitem-detail'
        ),
        url(
            r'^timeline/(?P<entity_pk>\w+)/$',
            api.ItemsTimeline.as_view(),
            name='items-timeline'
        ),
    )
    return urlpatterns
