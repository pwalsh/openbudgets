from django.conf.urls import patterns, include, url
from omuni.accounts.views import UserProfileDetailView, UserProfileUpdateView


urlpatterns = patterns('',

    url(r'^profile/(?P<slug>[-\w]+)/$',
        UserProfileDetailView.as_view(),
        name='user_profile_detail'
    ),
    url(r'^profile/(?P<slug>[-\w]+)/update/$',
        UserProfileUpdateView.as_view(),
        name='user_profile_update'
    ),
    url(r'^',
        include('registration.backends.default.urls')
    ),

)
