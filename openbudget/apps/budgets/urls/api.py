from django.conf.urls import patterns, url
from openbudget.apps.budgets.views import api


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
            api.TemplateNodeDetail.as_view(),
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
        url(
            r'^(?P<entity_pk>\w+)/timeline/(?P<node_pk>\w+)/$',
            api.NodeTimeline.as_view(),
            name='node-timeline'
        ),
    )
    return urlpatterns


def budgets():
    urlpatterns = patterns('',
        url(
            r'^$',
            api.BudgetList.as_view(),
            name='budget-list'
        ),
        url(
            r'^(?P<pk>\d+)/$',
            api.BudgetDetail.as_view(),
            name='budget-detail'
        ),
        url(
            r'^items/$',
            api.BudgetItemList.as_view(),
            name='budgetitem-list'
        ),
        url(
            r'^items/(?P<pk>\d+)/$',
            api.BudgetItemDetail.as_view(),
            name='budgetitem-detail'
        ),
    )
    return urlpatterns


def actuals():
    urlpatterns = patterns('',
        url(
            r'^$',
            api.ActualList.as_view(),
            name='actual-list'
        ),
        url(
            r'^(?P<pk>\d+)/$',
            api.ActualDetail.as_view(),
            name='actual-detail'
        ),
        url(
            r'^items/$',
            api.ActualItemList.as_view(),
            name='actualitem-list'
        ),
        url(
            r'^items/(?P<pk>\d+)/$',
            api.ActualItemDetail.as_view(),
            name='actualitem-detail'
        ),
    )
    return urlpatterns
