from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(help_text=_('We need your name to respond nicely!'))
    email = forms.EmailField(help_text=_('We can&apos;t get back to you without it.'))
    subject = forms.CharField(help_text=_('What is it about'))
    message = forms.CharField(widget=forms.Textarea, help_text=_('What do you want to tell us'))
