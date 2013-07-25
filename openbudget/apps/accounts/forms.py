from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm
from openbudget.apps.accounts.models import Account


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Email'), 'type': 'email'}),
        help_text=_('Press enter to finish'))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Enter Password'), 'type': 'password'}),
        help_text=_('Press enter to finish'))


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name', 'language')


class AccountCreationForm(UserCreationForm):
    """Our use of a custom user models requires we do this"""

    class Meta:
        model = Account
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            # See here:
            # https://groups.google.com/forum/?fromgroups#!topic/django-users/kOVEy9zYn5c
            # have to use self._meta.model
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class AccountChangeForm(UserChangeForm):
    """Our use of a custom user models requires we do this"""

    class Meta:
        model = Account
