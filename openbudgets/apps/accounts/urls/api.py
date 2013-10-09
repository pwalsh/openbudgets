from django.conf.urls import patterns, url
from openbudgets.apps.accounts.views import api


urlpatterns = patterns('',

    url(r'^$',
        api.AccountList.as_view(), name='account-list'),

    url(r'^(?P<pk>\d+)/$',
        api.AccountDetail.as_view(), name='account-detail'),

)
