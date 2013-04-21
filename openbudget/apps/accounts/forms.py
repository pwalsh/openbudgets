from django import forms
from openbudget.apps.accounts.models import Account


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name', 'language')
