"""Custom context processors for Omuni"""
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from openbudget.apps.accounts.forms import CustomAuthenticationForm, \
    CustomRegistrationForm, CustomPasswordResetForm, CustomPasswordChangeForm


def get_site(request):
    """Returns a Site object for the global request context"""
    # If we will later map multiple hosts to the project
    #host = request.get_host()
    #site = Site.objects.get(domain=host)

    # But, for now
    site = Site.objects.get(pk=1)

    return {'site': site}


def auth_forms(request):

    auth_forms = {}
    auth_forms['login_form'] = CustomAuthenticationForm
    auth_forms['registration_form'] = CustomRegistrationForm
    auth_forms['password_reset_form'] = CustomPasswordResetForm

    if request.user.is_authenticated:
        auth_forms['password_change_form'] = CustomPasswordChangeForm

    return auth_forms


def openbudgets(request):
    """Things that come from the settings of the project itself."""
    openbudgets = {}
    openbudgets['name'] = _(settings.OPENBUDGETS_NAME)

    return openbudgets
