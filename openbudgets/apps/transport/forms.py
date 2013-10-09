from django import forms
from django.utils.translation import ugettext_lazy as _


class FileImportForm(forms.Form):

    sourcefile = forms.FileField(help_text=_('Browse your file.'))
