from django.conf.urls import patterns, include, url
from omuni.accounts.views import UserProfileDetailView


urlpatterns = patterns('',

    url(r'^(?P<slug>[-\w]+)/$',
        UserProfileDetailView.as_view(),
        name='user_profile_detail'
    ),
    url(r'^$',
        include('registration.backends.default.urls')
    ),

)
