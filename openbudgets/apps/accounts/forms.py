from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, \
    PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm
from registration.forms import RegistrationFormUniqueEmail
from openbudgets.apps.accounts.models import Account


ENTER_FORM_HELP = _('Enter to finish')
EMAIL_REGEX = '[^@]+@[^@]+\.[a-zA-Z]{2,6}'


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Email'), 'type': 'email',
               'required': '', 'pattern': EMAIL_REGEX}), help_text=ENTER_FORM_HELP)

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter Password'), 'type': 'password',
               'required': '', 'pattern': '.{6,}'}), help_text=ENTER_FORM_HELP)


class CustomRegistrationForm(forms.Form):

    """Adapted from django-registration"""

    required_css_class = 'required'

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'), 'type': 'text', 'required': '',
               'pattern': '.{2,}'}), help_text=ENTER_FORM_HELP)

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Last Name'), 'type': 'text', 'required': '',
               'pattern': '.{2,}'}), help_text=ENTER_FORM_HELP)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Email'), 'type': 'email',
               'required': '', 'pattern': EMAIL_REGEX}), help_text=ENTER_FORM_HELP)

    email_confirm = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Confirm Email'), 'type': 'email',
               'required': '', 'pattern': EMAIL_REGEX}), help_text=ENTER_FORM_HELP)

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter Password'), 'type': 'password',
               'required': '', 'pattern': '.{6,}'}), help_text=ENTER_FORM_HELP)

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Confirm Password'), 'type': 'password',
               'required': '', 'pattern': '.{6,}'}), help_text=ENTER_FORM_HELP)

    def clean_email(self):

        existing = get_user_model().objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_('This email is already registered'))
        else:
            return self.cleaned_data['email']

    def clean(self):

        if 'email' in self.cleaned_data and 'email_confirm' in self.cleaned_data:
            if self.cleaned_data['email'] != self.cleaned_data['email_confirm']:
                raise forms.ValidationError(_('The emails do not match'))

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_('The passwords do not match'))

        return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Email'), 'type': 'email',
               'required': '', 'pattern': EMAIL_REGEX}), help_text=ENTER_FORM_HELP)


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter Current Password'), 'type': 'password',
               'required': '', 'pattern': '.{6,}'}), help_text=ENTER_FORM_HELP)

    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter New Password'), 'type': 'password',
               'required': '', 'pattern': '.{6,}'}), help_text=ENTER_FORM_HELP)

    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Confirm New Password'), 'type': 'password',
               'required': '', 'pattern': '.{6,}'}), help_text=ENTER_FORM_HELP)


class AccountNameForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'), 'type': 'text', 'required': '',
               'pattern': '.{2,}'}))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Last Name'), 'type': 'text', 'required': '',
               'pattern': '.{2,}'}))

    class Meta:
        model = Account
        fields = ('first_name', 'last_name')

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
