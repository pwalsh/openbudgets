from django import forms
from django.utils.translation import ugettext_lazy as _


ENTER_FORM_HELP = _('Enter to finish')
EMAIL_REGEX = '[^@]+@[^@]+\.[a-zA-Z]{2,6}'


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Name'), 'type': 'text',
               'required': '', 'pattern': '.{6,}'}), help_text=ENTER_FORM_HELP)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Email'), 'type': 'email',
               'required': '', 'pattern': EMAIL_REGEX}), help_text=ENTER_FORM_HELP)

    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '', 'cols': '', 'placeholder': _('Enter Message'), 'type': 'text',
               'required': '', 'pattern': '.{20,}'}), help_text=ENTER_FORM_HELP)
