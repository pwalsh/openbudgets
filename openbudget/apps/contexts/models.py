from django.db import models
from django.utils.translation import ugettext_lazy as _
from openbudget.apps.entities.models import Entity
from openbudget.commons.mixins.models import PeriodicModel, TimeStampedModel


class Context(TimeStampedModel, PeriodicModel):

    class Meta:
        abstract = True

    entity = models.ForeignKey(
        Entity
    )

class GeoSpatial(Context):
    """data for geospatial mapping of the entity"""
    sqm = models.PositiveIntegerField(
        _('Square Meters'),
        null=True,
        blank=True,
        help_text=_('The square meterage for this entity')
    )


class Demographic(Context):
    """data on the demographics of the entity"""
    population = models.PositiveIntegerField(
        _('Population'),
        null=True,
        blank=True,
        help_text=_('The population of this entity')
    )


class Education(Context):
    """"""
    high_school_count = models.PositiveIntegerField(
        _('High School Count'),
        null=True,
        blank=True,
        help_text=_('_')
    )
    primary_school_count = models.PositiveIntegerField(
        _('Primary School Count'),
        null=True,
        blank=True,
        help_text=_('_')
    )
    pre_school_count = models.PositiveIntegerField(
        _('Pre-School Count'),
        null=True,
        blank=True,
        help_text=_('_')
    )
