from django.conf.urls import patterns, url
from openbudget.entities.views import EntityDetailView, EntityListView
from openbudget.budgets.views import BudgetDetailView, BudgetItemDetailView, ActualDetailView, ActualItemDetailView


urlpatterns = patterns('',

    url(r'^$',
        EntityListView.as_view(),
        name='entity_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        EntityDetailView.as_view(),
        name='entity_detail'
    ),
    url(r'^budget/(?P<slug>[-\w]+)/$',
        BudgetDetailView.as_view(),
        name='budget_detail'
    ),
    url(r'^actual/(?P<slug>[-\w]+)/$',
        ActualDetailView.as_view(),
        name='actual_detail'
    ),
    url(r'^budget/item/(?P<slug>[-\w]+)/$',
        BudgetItemDetailView.as_view(),
        name='budget_item_detail'
    ),
    url(r'^actual/item/(?P<slug>[-\w]+)/$',
        ActualItemDetailView.as_view(),
        name='actual_item_detail'
    ),

)
