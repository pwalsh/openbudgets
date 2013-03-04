from django.conf.urls import patterns, url
from openbudget.govts.views import GeoPolDetailView, GeoPolListView
from openbudget.budgets.views import BudgetDetailView, BudgetItemDetailView, ActualDetailView, ActualItemDetailView


urlpatterns = patterns('',

    url(r'^$',
        GeoPolListView.as_view(),
        name='geopol_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        GeoPolDetailView.as_view(),
        name='geopol_detail'
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
