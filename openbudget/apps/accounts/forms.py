from django import forms
from django.utils.translation import ugettext_lazy as _
from openbudget.apps.accounts.models import Account


class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(
            max_length=30,
            help_text=_('Your username.'),
            required=True
        )

        self.fields['email'] = forms.EmailField(
            max_length=75,
            help_text=_('Your email address.'),
            required=True
        )

        self.fields['first_name'] = forms.CharField(
            max_length=30,
            help_text=_('Your first name.'),
            required=False
        )

        self.fields['last_name'] = forms.CharField(
            max_length=30,
            help_text=_('Your last name.'),
            required=False
        )

    class Meta:
        model = Account
        exclude = ['user', 'uuid']
