from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from openbudget.apps.accounts.models import Account


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
