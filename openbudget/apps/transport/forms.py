from django import forms
from django.utils.translation import ugettext_lazy as _


# TODO: Lock down for admin access only
class FileImportForm(forms.Form):
    sourcefile = forms.FileField(help_text=_('Browse your file.'))
