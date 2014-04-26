"""Custom context processors for Omuni"""
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from openbudgets.apps.accounts.forms import CustomAuthenticationForm, \
    CustomRegistrationForm, CustomPasswordResetForm, CustomPasswordChangeForm
from openbudgets.apps.pages.forms import ContactForm


def site(request):
    """Returns a Site object for the global request context"""
    # If we will later map multiple hosts to the project
    #host = request.get_host()
    #site = Site.objects.get(domain=host)
    # But, for now
    site = Site.objects.get(pk=1)

    return {'site': site}


def forms(request):

    forms = {}
    forms['login_form'] = CustomAuthenticationForm
    forms['registration_form'] = CustomRegistrationForm
    forms['password_reset_form'] = CustomPasswordResetForm
    forms['contact_form'] = ContactForm

    if request.user.is_authenticated:
        forms['password_change_form'] = CustomPasswordChangeForm

    return forms


def openbudgets(request):
    """Things that come from the settings of the project itself."""

    openbudgets = {}
    openbudgets['app_name'] = _(settings.OPENBUDGETS_NAME_APP)
    openbudgets['app_name_list'] = openbudgets['app_name'].split()
    openbudgets['sponsor_name'] = _(settings.OPENBUDGETS_NAME_SPONSOR)
    openbudgets['sponsor_name_list'] = openbudgets['sponsor_name'].split()
    openbudgets['avatar_anon'] = settings.OPENBUDGETS_AVATAR_ANON
    openbudgets['with_api'] = settings.OPENBUDGETS_API['enable']

    return openbudgets
