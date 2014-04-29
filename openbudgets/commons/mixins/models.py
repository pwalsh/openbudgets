from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuidfield import UUIDField


class ClassMethodMixin(object):

    """Adds commonly used class methods to inheriting models."""

    @classmethod
    def get_class_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

    @classmethod
    def get_verbose_name_plural(cls):
        return cls._meta.verbose_name_plural


class TimeStampMixin(models.Model):

    """Adds timestamps to inheriting models."""

    class Meta:
        abstract = True

    created_on = models.DateTimeField(
        _('Created On'),
        db_index=True,
        auto_now_add=True,
        editable=False,)

    last_modified = models.DateTimeField(
        _('Last Modified'),
        db_index=True,
        auto_now=True,
        editable=False,)


class UUIDMixin(models.Model):

    """Adds a uuid field to inheriting models."""

    class Meta:
        abstract = True

    uuid = UUIDField(
        db_index=True,
        auto=True,
        hyphenate=True,)


class UUIDPKMixin(models.Model):

    """Adds a primary key called id, where id is a uuid, to inheriting models."""

    class Meta:
        abstract = True

    id = UUIDField(
        db_index=True,
        auto=True,
        primary_key=True,
        hyphenate=True,)


class SelfParentMixin(models.Model):

    """Adds a parent which is self to inheriting models.

    The mixin also exposes:

    * a `children` queryset accessor, e.g.: .children.all()
    * an `ancestors` method that returns a queryset

    """

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        editable=False,
        related_name='children',)

    @property
    def ancestors(self):
        return self.get_ancestors()

    def get_ancestors(self):

        if self.parent is None:
            return self.__class__.objects.none()
        qs = self.__class__.objects.filter(pk=self.parent.pk) | self.parent.get_ancestors()

        return qs.order_by('depth')

    class Meta:
        abstract = True


class PeriodStartMixin(models.Model):

    """Adds to add a period_start field to inheriting models.

    The primary use of this mixin is for model objects with data that applies
    over a period of time, and where the applicable period is only determined by
    the presence of another object with a future-dated value for period_start.
    """

    class Meta:
        abstract = True

    period_start = models.DateField(
        _('Period Start'),
        db_index=True,
        null=True,
        blank=True,
        help_text=_('Period start for %(class)s'),)


class PeriodicMixin(PeriodStartMixin):

    """Add period start and period end fields to inheriting models."""

    class Meta:
        abstract = True

    period_end = models.DateField(
        _('Period End'),
        db_index=True,
        null=True,
        blank=True,
        help_text=_('Period end for this %(class)s'),)

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

        return value
