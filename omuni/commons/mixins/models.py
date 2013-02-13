from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuidfield import UUIDField


class TimeStampedModel(object):
    """A simple mixin to timestamp models that inherit from it"""

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


class UUIDModel(object):
    """A simple mixin to universally uniquely identify models that inherit from it"""

    uuid = UUIDField(
        auto=True
    )