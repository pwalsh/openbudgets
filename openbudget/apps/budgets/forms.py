from django import forms
from django.utils.translation import ugettext_lazy as _
from openbudget.apps.budgets.models import Annotation


class AnnotationForm(forms.ModelForm):

    class Meta:
        model = Annotation
