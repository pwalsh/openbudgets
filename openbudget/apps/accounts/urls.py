from django.conf.urls import patterns, include, url
from openbudget.apps.accounts.views import UserProfileDetailView, UserProfileUpdateView


urlpatterns = patterns('',

    url(r'^auth/',
        include('registration.backends.default.urls')
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        UserProfileDetailView.as_view(),
        name='account_detail'
    ),
    url(r'^(?P<slug>[-\w]+)/update/$',
        UserProfileUpdateView.as_view(),
        name='account_update'
    ),
)
