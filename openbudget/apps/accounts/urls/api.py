from django.conf.urls import patterns, url
from openbudget.apps.accounts.views import api


urlpatterns = patterns('',

    url(r'^$',
        api.AccountList.as_view(),
        name='account-list'
    ),
    url(r'^(?P<uuid>\w+)/$',
        api.AccountDetail.as_view(),
        name='account-detail'
    ),
)
