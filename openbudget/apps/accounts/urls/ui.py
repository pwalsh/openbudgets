from django.conf.urls import patterns, include, url
from openbudget.apps.accounts.views.ui import AccountDetailView, AccountUpdateView


urlpatterns = patterns('',

    url(r'^auth/',
        include('registration.backends.default.urls')
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        AccountDetailView.as_view(),
        name='account_detail'
    ),
    url(r'^(?P<slug>[-\w]+)/update/$',
        AccountUpdateView.as_view(),
        name='account_update'
    ),
)
