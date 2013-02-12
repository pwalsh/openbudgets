from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    """A simple mixin to timestamp models that inherit from it"""

    class Meta:
        abstract = True

    created_on = models.DateTimeField(
        _('Created on'),
        auto_now_add=True,
        editable=False
    )
    last_modified = models.DateTimeField(
        _('Last modified'),
        auto_now=True,
        editable=False
    )
