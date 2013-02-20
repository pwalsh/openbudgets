from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from omuni.api.views import GeoPoliticalEntityList, GeoPoliticalEntityDetail, BudgetTemplateDetail, BudgetTemplateNodeDetail, BudgetList, BudgetDetail, BudgetItemList, BudgetItemDetail, ActualList, ActualDetail, ActualItemList, ActualItemDetail


urlpatterns = patterns('omuni.api.views',
    url(r'^$',
        'api_root',
        name='api'
    ),
    url(r'^geopols/$',
        GeoPoliticalEntityList.as_view(),
        name='geopolitcalentity-list'
    ),
    url(r'^geopol/(?P<pk>\d+)/$',
        GeoPoliticalEntityDetail.as_view(),
        name='geopoliticalentity-detail'
    ),
    url(r'^budget/template/(?P<pk>\d+)/$',
        BudgetTemplateDetail.as_view(),
        name='budgettemplate-detail'
    ),
    url(r'^budget/template/node/(?P<pk>\d+)/$',
        BudgetTemplateNodeDetail.as_view(),
        name='budgettemplatenode-detail'
    ),
    url(r'^budgets/$',
        BudgetList.as_view(),
        name='budget-list'
    ),
    url(r'^budget/(?P<pk>\d+)/$',
        BudgetDetail.as_view(),
        name='budget-detail'
    ),
    url(r'^budgetitems/$',
        BudgetItemList.as_view(),
        name='budgetitem-list'
    ),
    url(r'^budgetitem/(?P<pk>\d+)/$',
        BudgetItemDetail.as_view(),
        name='budgetitem-detail'
    ),
    url(r'^actuals/$',
        ActualList.as_view(),
        name='actual-list'
    ),
    url(r'^actual/(?P<pk>\d+)/$',
        ActualDetail.as_view(),
        name='actual-detail'
    ),
    url(r'^actualitems/$',
        ActualItemList.as_view(),
        name='actualitem-list'
    ),
    url(r'^actualitem/(?P<pk>\d+)/$',
        ActualItemDetail.as_view(),
        name='actualitem-detail'
    ),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
