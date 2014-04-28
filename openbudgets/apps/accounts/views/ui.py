import hashlib
import random
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, UpdateView
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from braces.views import LoginRequiredMixin
from registration.views import RegistrationView
from registration.models import RegistrationProfile
from registration import signals
from openbudgets.apps.accounts.models import Account
from openbudgets.apps.accounts.forms import AccountNameForm, AccountForm, \
    CustomRegistrationForm, CustomAuthenticationForm, CustomPasswordChangeForm,\
    CustomPasswordResetForm
from openbudgets.commons.mixins.views import UserDataObjectMixin, JSONResponseMixin


class AccountDetailView(LoginRequiredMixin, UserDataObjectMixin, DetailView):
    model = Account
    template_name = 'accounts/account_detail.html'
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context['name_form'] = AccountNameForm(instance=self.request.user)
        return context


class AccountUpdateView(LoginRequiredMixin, UserDataObjectMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_update.html'
    slug_field = 'uuid'


class AccountRegistrationView(JSONResponseMixin, RegistrationView):

    form_class = CustomRegistrationForm

    def form_invalid(self, form, request=None):

        response = super(AccountRegistrationView, self).form_invalid(form)

        if self.request.is_ajax():

            # we are simplifying the errors because of the available UI space.
            #
            # 1. Check for email availability, return if error
            #
            # 2. Check for cross-field errors which here means:
            #
            #   (a) if the emails entering are not matching, return if error
            #   (b) if the passwords entering are not matching, return if error

            if 'email' in dict(form.errors):

                chosen_error = form.errors['email'][0]

            else:

                chosen_error = form.errors['__all__'][0]

            data = chosen_error

            # JQuery is expecting a string, not an object.
            #return self.render_to_json_response(data, status=400)
            return HttpResponse(data)

        else:

            return response

    def form_valid(self, request, form):

        response = super(AccountRegistrationView, self).form_valid(request, form)

        if self.request.is_ajax():
            data = {
                'data': _('Check your email to proceed'),
            }

            return self.render_to_json_response(data)

        else:

            return response

    def register(self, request, **cleaned_data):

        first_name, last_name, email, password = cleaned_data['first_name'], \
                                                 cleaned_data['last_name'], \
                                                 cleaned_data['email'], \
                                                 cleaned_data['password1']
        site = Site.objects.get_current()

        # Custom user creation, as django-registration has username hardcoded.
        # this is usually wrapped in a model method.
        new_user = get_user_model().objects.create_user(email, first_name,
                                                        last_name, password)
        new_user.is_active = False

        new_user.save()

        # Customizing django-registration's create_profile method, as it
        # relies on the username
        # this is usually wrapped in a model method.
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]

        email = new_user.email

        if isinstance(email, unicode):
            email = email.encode('utf-8')

        activation_key = hashlib.sha1(salt+email).hexdigest()

        registration_profile = RegistrationProfile.objects.create(
            user=new_user, activation_key=activation_key)

        registration_profile.send_activation_email(site)

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):

        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):

        return ('registration_complete', (), {})


@sensitive_post_parameters()
@csrf_protect
@never_cache
def account_login(request, template_name='registration/login.html',
                  redirect_field_name=REDIRECT_FIELD_NAME,
                  authentication_form=CustomAuthenticationForm,
                  current_app=None, extra_context=None):

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":

        form = authentication_form(data=request.POST)
        next = request.POST['next']

        if form.is_valid():

            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            if request.is_ajax():

                data = {
                    'data': _('Success'),
                    'next': next
                }

                return HttpResponse(json.dumps(data), status=200)

            return HttpResponseRedirect(redirect_to)

        # TODO: check this out further. we have no form.not_valid() method
        elif request.is_ajax():

            data = {
                'data': _('Incorrect credentials'),
                'next': next
            }

            # JQuery is expecting a string, not an object
            return HttpResponse(data['data'], status=400)

    else:

        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }

    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@sensitive_post_parameters()
@csrf_protect
@login_required
def account_password_change(request,
                            template_name='registration/password_change_form.html',
                            post_change_redirect=None,
                            password_change_form=CustomPasswordChangeForm,
                            current_app=None, extra_context=None):

    if post_change_redirect is None:

        post_change_redirect = reverse('django.contrib.auth.views.password_change_done')

    if request.method == "POST":

        form = password_change_form(user=request.user, data=request.POST)
        next = request.POST['next']

        if form.is_valid():

            form.save()

            if request.is_ajax():

                data = {
                    'data': _('Your password has been changed'),
                    'next': next
                }

                return HttpResponse(json.dumps(data), status=200)

            return HttpResponseRedirect(post_change_redirect)

        # TODO: check this out further. we have no form.not_valid() method
        elif request.is_ajax():

            data = {
                'data': _('The form has errors. try again'),
                'next': next
            }

            # JQuery is expecting a string, not an object
            return HttpResponse(data['data'], status=400)

    else:

        form = password_change_form(user=request.user)

    context = {
        'form': form,
    }

    if extra_context is not None:

        context.update(extra_context)

    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@csrf_protect
def account_password_reset(request, is_admin_site=False,
                           template_name='registration/password_reset_form.html',
                           email_template_name='registration/password_reset_email.html',
                           subject_template_name='registration/password_reset_subject.txt',
                           password_reset_form=CustomPasswordResetForm,
                           token_generator=default_token_generator,
                           post_reset_redirect=None,
                           from_email=None,
                           current_app=None,
                           extra_context=None):

    if post_reset_redirect is None:

        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')

    if request.method == "POST":

        form = password_reset_form(request.POST)
        next = request.POST['next']

        if form.is_valid():

            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }

            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)

            if request.is_ajax():

                data = {
                    'data': _('Success. Check your inbox'),
                    'next': next
                }

                return HttpResponse(json.dumps(data), status=200)

            return HttpResponseRedirect(post_reset_redirect)

        # TODO: check this out further. we have no form.not_valid() method
        elif request.is_ajax():

            data = {
                'data': _('Unknown email address'),
                'next': next
            }

            # JQuery is expecting a string, not an object
            return HttpResponse(data['data'], status=400)

    else:

        form = password_reset_form()

    context = {
        'form': form,
    }

    if extra_context is not None:

        context.update(extra_context)

    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
