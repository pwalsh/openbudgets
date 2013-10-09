from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuidfield import UUIDField


class ClassMethodMixin(object):
    """A mixin for commonly used classmethods on models."""

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    @classmethod
    def get_verbose_name(cls):
        value = cls._meta.verbose_name
        return value

    @classmethod
    def get_verbose_name_plural(cls):
        value = cls._meta.verbose_name_plural
        return value


class TimeStampedMixin(models.Model):
    """A mixin to add timestamps to models that inherit it."""

    created_on = models.DateTimeField(
        _('Created on'),
        db_index=True,
        auto_now_add=True,
        editable=False
    )
    last_modified = models.DateTimeField(
        _('Last modified'),
        db_index=True,
        auto_now=True,
        editable=False
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """A mixin to add a UUID to models that inherit it."""

    uuid = UUIDField(
        db_index=True,
        auto=True
    )

    class Meta:
        abstract = True


class UUIDPKMixin(models.Model):
    """A mixin to add a UUID as the primary key of models that inherit it."""

    id = UUIDField(
        db_index=True,
        auto=True,
        primary_key=True
    )

    class Meta:
        abstract = True


class PeriodStartMixin(models.Model):
    """A mixin to add a period_start field to models that inherit it.

    The primary use of this mixin is for model objects with data that applies
    over a period of time, and where the applicable period is only determined by
    the presence of another object with a future-dated value for period_start.

    Example: CBS data (valid until the next dataset), official budget template for
    municipalities in Israel (valid until a new template will come to
    replace/extend the existing one.)
    """

    period_start = models.DateField(
        _('Period start'),
        db_index=True,
        null=True,
        blank=True,
        help_text=_('The start date for this %(class)s'),
    )

    class Meta:
        abstract = True


class PeriodicMixin(PeriodStartMixin):
    """A mixin to add a defined period of validity to models that inherit it."""

    period_end = models.DateField(
        _('Period end'),
        db_index=True,
        null=True,
        blank=True,
        help_text=_('The end date for this %(class)s')
    )

    @property
    def period(self):
        """Get the applicable period for this object.

        In the current case of yearly ranges, returns datetime.year object.
        """

        # TODO: Support ranges other than yearly, including multiple ranges.

        value = None
        ranges = settings.OPENBUDGETS_PERIOD_RANGES

        if len(ranges) == 1 and 'yearly' in ranges:
            value = self.period_start.year
        else:
            # TODO: Verify - in the current codebase, we should never get here.
            pass

        return value

    class Meta:
        abstract = True
