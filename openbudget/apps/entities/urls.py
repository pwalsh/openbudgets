from django.conf.urls import patterns, url
from openbudget.apps.entities.views import EntityDetailView, EntityListView
from openbudget.apps.budgets.views import BudgetDetailView, BudgetTemplateDetailView, BudgetTemplateListView, BudgetItemDetailView, ActualDetailView, ActualItemDetailView


urlpatterns = patterns('',

    url(r'^budget-templates/$',
        BudgetTemplateListView.as_view(),
        name='budget_template_list'
    ),
    url(r'^budget-template/(?P<slug>[-\w]+)/$',
        BudgetTemplateDetailView.as_view(),
        name='budget_template_detail'
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
    url(r'^$',
        EntityListView.as_view(),
        name='entity_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        EntityDetailView.as_view(),
        name='entity_detail'
    ),

)
