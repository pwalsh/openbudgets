from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuidfield import UUIDField


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


class UUIDModel(models.Model):
    """A simple mixin to add a uuid to models that inherit from it"""

    class Meta:
        abstract = True

    uuid = UUIDField(
        auto=True
    )


class PeriodicModel(models.Model):

    class Meta:
        abstract = True

    period_start = models.DateField(
        _('Period start'),
        help_text=_('The start date for this %(class)s')
    )
    period_end = models.DateField(
        _('Period end'),
        help_text=_('The end date for this %(class)s')
    )

    #TODO: implement a shortcut from period_start/end to year
    @property
    def period(self):
        # TODO: Write a smarter method for the general use case
        # naive, just for current purposes
        tmp = self.period_end - self.period_start
        if tmp.days <= 365:
            return self.period_start.year
        else:
            return unicode(self.period_start.year) + ' - ' + self.period_end.year