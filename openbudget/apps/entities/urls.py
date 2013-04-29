from django.conf.urls import patterns, url
from openbudget.apps.entities.views import EntityDetailView, EntityListView
from openbudget.apps.budgets.views import BudgetDetailView, BudgetTemplateDetailView, BudgetTemplateListView, BudgetItemDetailView, ActualDetailView, ActualItemDetailView


urlpatterns = patterns('',

    url(r'^$',
        EntityListView.as_view(),
        name='entity_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        EntityDetailView.as_view(),
        name='entity_detail'
    ),

)
