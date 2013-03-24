from django.conf.urls import patterns, url
from openbudget.apps.budgets.views import budget_browser


urlpatterns = patterns('',
    url(r'^browser/$',
        budget_browser,
        name='budget_browser'
    ),
)