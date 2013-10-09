from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib.auth import views as auth_views

from registration.backends.default.views import ActivationView
from openbudgets.apps.accounts.views.ui import AccountDetailView, \
    AccountUpdateView, AccountRegistrationView, account_login, \
    account_password_change, account_password_reset


urlpatterns = patterns('',

    url(r'^activate/complete/$',
       TemplateView.as_view(template_name='registration/activation_complete.html'),
       name='registration_activation_complete'),

    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(), name='registration_activate'),

    url(r'^register/$',
        AccountRegistrationView.as_view(), name='registration_register'),

    url(r'^register/complete/$',
       TemplateView.as_view(template_name='registration/registration_complete.html'),
       name='registration_complete'),

    url(r'^register/closed/$',
       TemplateView.as_view(template_name='registration/registration_closed.html'),
       name='registration_disallowed'),

    url(r'^login/$',
       account_login, {'template_name': 'registration/login.html'}, name='auth_login'),

    url(r'^logout/$',
       auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),

    url(r'^password/change/$',
        account_password_change,name='auth_password_change'),

    url(r'^password/change/done/$',
       auth_views.password_change_done, name='auth_password_change_done'),

    url(r'^password/reset/$',
       account_password_reset, name='auth_password_reset'),

    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm, name='auth_password_reset_confirm'),

    url(r'^password/reset/complete/$',
       auth_views.password_reset_complete, name='auth_password_reset_complete'),

    url(r'^password/reset/done/$',
       auth_views.password_reset_done, name='auth_password_reset_done'),

    url(r'^(?P<slug>[-\w]+)/$',
        AccountDetailView.as_view(), name='account_detail'),

    url(r'^(?P<slug>[-\w]+)/update/$',
        AccountUpdateView.as_view(), name='account_update'),

)
