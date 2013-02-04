from django.conf.urls import patterns, url
from omuni.govts.views import GeoPolDetailView, GeoPolListView
from omuni.budgets.views import BudgetDetailView


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

)
