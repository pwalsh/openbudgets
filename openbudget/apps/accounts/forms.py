from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, \
    PasswordChangeForm
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm
from registration.forms import RegistrationFormUniqueEmail
from openbudget.apps.accounts.models import Account


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Email'), 'type': 'email'}),
        help_text=_('Press enter to finish'))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter Password'), 'type': 'password'}),
        help_text=_('Press enter to finish'))


class CustomRegistrationForm(forms.Form):
    """Adapted from django-registration"""

    required_css_class = 'required'

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'), 'type': 'text'}),
        help_text=_('Press enter to finish'))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Last Name'), 'type': 'text'}),
        help_text=_('Press enter to finish'))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Email'), 'type': 'email'}),
        help_text=_('Press enter to finish'))
    email_confirm = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Confirm Email'), 'type': 'email'}),
        help_text=_('Press enter to finish'))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter Password'), 'type': 'password'}),
        help_text=_('Press enter to finish'))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Confirm Password'), 'type': 'password'}),
        help_text=_('Press enter to finish'))

    def clean_email(self):

        existing = get_user_model().objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']

    def clean(self):

        if 'email' in self.cleaned_data and 'email_confirm' in self.cleaned_data:
            if self.cleaned_data['email'] != self.cleaned_data['email_confirm']:
                raise forms.ValidationError(_("The two email fields didn't match."))

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))

        return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Email'), 'type': 'email'}),
        help_text=_('Press enter to finish'))


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter Current Password'), 'type': 'password'}),
        help_text=_('Press enter to finish'))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter New Password'), 'type': 'password'}),
        help_text=_('Press enter to finish'))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Confirm New Password'), 'type': 'password'}),
        help_text=_('Press enter to finish'))


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'language')


class AccountCreationForm(UserCreationForm):
    """Our use of a custom user models requires we do this"""

    class Meta:
        model = Account
        fields = ("email",)

    def clean_username(self):
        username = self.cleaned_data["email"]
        try:
            # See here:
            # https://groups.google.com/forum/?fromgroups#!topic/django-users/kOVEy9zYn5c
            # have to use self._meta.model
            self._meta.model._default_manager.get(email=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class AccountChangeForm(UserChangeForm):
    """Our use of a custom user models requires we do this"""

    class Meta:
        model = Account
