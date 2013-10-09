from django.conf.urls import patterns, url
from openbudgets.apps.pages.views import HomeView, ContactView, PageView


urlpatterns = patterns('',

    url(r'^$',
        HomeView.as_view(), name='home'),

    url(r'^contact/$',
        ContactView.as_view(), name='contact'),

    url(r'^(?P<slug>[-\w]+)/$',
        PageView.as_view(), name='page'),

)
