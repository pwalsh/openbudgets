from django.conf.urls import patterns, url
from openbudget.apps.budgets.views.ui import BudgetTemplateListView, BudgetTemplateDetailView, BudgetListView, BudgetDetailView, ActualListView, ActualDetailView, BudgetItemDetailView, ActualItemDetailView, budget_browser


urlpatterns = patterns('',

    url(r'^browser/$',
        budget_browser,
        name='budget_browser'
    ),
    url(r'^templates/$',
        BudgetTemplateListView.as_view(),
        name='template_list'
    ),
    url(r'^templates/(?P<slug>[-\w]+)/$',
        BudgetTemplateDetailView.as_view(),
        name='template_detail'
    ),
    url(r'^budgets/$',
        BudgetListView.as_view(),
        name='budget_list'
    ),
    url(r'^budgets/(?P<entity_slug>[-\w]+)/(?P<period>[-\w]+)/$',
        BudgetDetailView.as_view(),
        name='budget_detail'
    ),
    url(r'^actuals/$',
        ActualListView.as_view(),
        name='actual_list'
    ),
    url(r'^actuals/(?P<entity_slug>[-\w]+)/(?P<period>[-\w]+)/$',
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
