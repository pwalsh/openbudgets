from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from omuni.api.views import GeoPoliticalEntityList, GeoPoliticalEntityDetail, BudgetList, BudgetDetail


urlpatterns = patterns('omuni.api.views',
    url(r'^$',
        'api_root'
    ),
    url(r'^geopols/$',
        GeoPoliticalEntityList.as_view(),
        name='geopolitcalentity-list'
    ),
    url(r'^geopol/(?P<pk>\d+)/$',
        GeoPoliticalEntityDetail.as_view(),
        name='geopoliticalentity-detail'
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
        BudgetList.as_view(),
        name='budgetitem-list'
    ),
    url(r'^budgetitem/(?P<pk>\d+)/$',
        BudgetDetail.as_view(),
        name='budgetitem-detail'
    ),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
