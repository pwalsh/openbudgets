from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from openbudget.api import views


urlpatterns = patterns('openbudget.api.views',
    url(r'^$',
        'api_root',
        name='api'
    ),
    url(r'^auth/',
        include('provider.oauth2.urls', namespace='oauth2')
    ),
    url(r'^domain/$',
        views.DomainList.as_view(),
        name='domain-list'
    ),
    url(r'^domain/(?P<pk>\d+)/$',
        views.DomainDetail.as_view(),
        name='domain-detail'
    ),
    url(r'^division/$',
        views.DivisionList.as_view(),
        name='division-list'
    ),
    url(r'^division/(?P<pk>\d+)/$',
        views.DivisionDetail.as_view(),
        name='division-detail'
    ),
    url(r'^entity/$',
        views.EntityList.as_view(),
        name='entity-list'
    ),
    url(r'^entity/(?P<pk>\d+)/$',
        views.EntityDetail.as_view(),
        name='entity-detail'
    ),
    url(r'^template/$',
        views.TemplateList.as_view(),
        name='budgettemplate-list'
    ),
    url(r'^template/(?P<pk>\d+)/$',
        views.TemplateDetail.as_view(),
        name='budgettemplate-detail'
    ),
    url(r'^budget/template/node/(?P<pk>\d+)/$',
        views.TemplateNodeDetail.as_view(),
        name='templatenode-detail'
    ),
    url(r'^budget/$',
        views.BudgetList.as_view(),
        name='budget-list'
    ),
    url(r'^budget/(?P<pk>\d+)/$',
        views.BudgetDetail.as_view(),
        name='budget-detail'
    ),
    url(r'^budgetitem/$',
        views.BudgetItemList.as_view(),
        name='budgetitem-list'
    ),
    url(r'^budgetitem/(?P<pk>\d+)/$',
        views.BudgetItemDetail.as_view(),
        name='budgetitem-detail'
    ),
    url(r'^actual/$',
        views.ActualList.as_view(),
        name='actual-list'
    ),
    url(r'^actual/(?P<pk>\d+)/$',
        views.ActualDetail.as_view(),
        name='actual-detail'
    ),
    url(r'^actualitem/$',
        views.ActualItemList.as_view(),
        name='actualitem-list'
    ),
    url(r'^actualitem/(?P<pk>\d+)/$',
        views.ActualItemDetail.as_view(),
        name='actualitem-detail'
    ),
    url(r'^nodes/latest/(?P<entity_pk>\w+)/$',
        views.TemplateNodesListLatest.as_view(),
        name='node-list-latest'
    ),
    url(r'^(?P<entity_pk>\w+)/timeline/(?P<node_pk>\w+)/$',
        views.NodeTimeline.as_view(),
        name='node-timeline'
    ),
    url(r'^project/$',
        views.ProjectCreate.as_view(),
        name='project-create'
    ),
    url(r'^project/(?P<project_pk>\w+)/$',
        views.ProjectAct.as_view(),
        name='project-act'
    ),
)

# Format suffixes
urlpatterns = format_suffix_patterns(
    urlpatterns, allowed=['json', 'api']
)

# Default login/logout views
urlpatterns += patterns('',
    url(r'^api-auth/',
        include('rest_framework.urls',
            namespace='rest_framework'
        )
    )
)
