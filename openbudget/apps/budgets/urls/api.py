from django.conf.urls import patterns, url
from openbudget.apps.budgets.views.api import TemplateList, TemplateDetail, \
    TemplateNodeDetail, BudgetList, BudgetDetail, BudgetItemList, \
    BudgetItemDetail, ActualList, ActualDetail, ActualItemList, \
    ActualItemDetail, TemplateNodesListLatest, NodeTimeline


urlpatterns = patterns('',

    url(r'^templates/$',
        TemplateList.as_view(),
        name='template-list'
    ),
    url(r'^templates/(?P<pk>\d+)/$',
        TemplateDetail.as_view(),
        name='template-detail'
    ),
    url(r'^template-nodes/(?P<pk>\d+)/$',
        TemplateNodeDetail.as_view(),
        name='templatenode-detail'
    ),
    url(r'^budgets/$',
        BudgetList.as_view(),
        name='budget-list'
    ),
    url(r'^budgets/(?P<pk>\d+)/$',
        BudgetDetail.as_view(),
        name='budget-detail'
    ),
    url(r'^budget-items/$',
        BudgetItemList.as_view(),
        name='budgetitem-list'
    ),
    url(r'^budget-items/(?P<pk>\d+)/$',
        BudgetItemDetail.as_view(),
        name='budgetitem-detail'
    ),
    url(r'^actuals/$',
        ActualList.as_view(),
        name='actual-list'
    ),
    url(r'^actuals/(?P<pk>\d+)/$',
        ActualDetail.as_view(),
        name='actual-detail'
    ),
    url(r'^actual-items/$',
        ActualItemList.as_view(),
        name='actualitem-list'
    ),
    url(r'^actual-items/(?P<pk>\d+)/$',
        ActualItemDetail.as_view(),
        name='actualitem-detail'
    ),
    url(r'^nodes/latest/(?P<entity_pk>\w+)/$',
        TemplateNodesListLatest.as_view(),
        name='node-list-latest'
    ),
    url(r'^(?P<entity_pk>\w+)/timeline/(?P<node_pk>\w+)/$',
        NodeTimeline.as_view(),
        name='node-timeline'
    ),

)
