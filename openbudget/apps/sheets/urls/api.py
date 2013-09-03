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
            r'^nodes/$',
            api.TemplateNodeList.as_view(),
            name='templatenode-list'
        ),
        url(
            r'^nodes/(?P<pk>[-\w]+)/$',
            api.TemplateNodeDetail.as_view(),
            name='templatenode-detail'
        ),
        url(
            r'^(?P<pk>[-\w]+)/$',
            api.TemplateDetail.as_view(),
            name='template-detail'
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
            r'^(?P<pk>[-\w]+)/$',
            api.SheetDetail.as_view(),
            name='sheet-detail'
        ),
        url(
            r'^items/$',
            api.SheetItemList.as_view(),
            name='sheetitem-list'
        ),
        url(
            r'^items/(?P<pk>[-\w]+)/$',
            api.SheetItemDetail.as_view(),
            name='sheetitem-detail'
        ),
        url(
            r'^items/(?P<pk>[-\w]+)/comments/$',
            api.SheetItemCommentListCreate.as_view(),
            name='sheetitemcomment-list-create'
        ),
        url(
            r'^timeline/(?P<entity_pk>[-\w]+)/$',
            api.SheetItemTimeline.as_view(),
            name='sheetitem-timeline'
        ),
    )
    return urlpatterns
