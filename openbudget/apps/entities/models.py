from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel, \
    ClassMethodMixin
from openbudget.commons.utilities import get_ultimate_parent


class DomainManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map(self):
        return self.select_related().prefetch_related('divisions')


class Domain(TimeStampedModel, ClassMethodMixin):
    """Domain is the base context for our relational model of entities.

    Entities always belong to a domain, and are structured via Divisions.

    The ability to have multiple domains allows an Open Budget instance to
    support adjacent or even unrelated data sets. See the docs for more info.
    """

    MEASUREMENT_SYSTEMS = (
        ('metric', _('Metric')),
        ('imperial', _('Imperial'))
    )
    GROUND_SURFACE_UNITS = (
        ('default', _('Default')),
        ('dunams', _('Dunams'))
    )
    CURRENCIES = (
        ('usd', _('&#36;')),
        ('ils', _('&#8362;'))
    )

    objects = DomainManager()

    name = models.CharField(
        _('Name'),
        db_index=True,
        max_length=255,
        unique=True,
        help_text=_('The name of this domain.')
    )
    measurement_system = models.CharField(
        _('Measurement System'),
        max_length=8,
        choices=MEASUREMENT_SYSTEMS,
        default=MEASUREMENT_SYSTEMS[0][0],
        help_text=_('The applicable measurement unit for this domain.')
    )
    ground_surface_unit = models.CharField(
        _('Ground Surface Unit'),
        max_length=25,
        choices=GROUND_SURFACE_UNITS,
        default=GROUND_SURFACE_UNITS[0][0],
        help_text=_('Rarely to be touched, this field is for countries, like '
                    'Israel, that use special units for measuring ground.')
    )
    currency = models.CharField(
        _('Currency'),
        max_length=3,
        choices=CURRENCIES,
        default=CURRENCIES[0][0],
        help_text=_('The currency used for budgeting in this domain.')
    )

    @property
    def entities(self):
        value = Entity.objects.related_map().filter(division__domain=self)
        return value

    class Meta:
        ordering = ['name']
        verbose_name = _('domain')
        verbose_name_plural = _('domains')

    def __unicode__(self):
        return self.name


class DivisionManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map(self):
        return self.select_related().prefetch_related('entities')


class Division(TimeStampedModel, ClassMethodMixin):
    """Division divides the domain into logical groupings to model structure."""

    objects = DivisionManager()

    domain = models.ForeignKey(
        Domain,
        related_name='divisions',
        help_text=_('The domain that this division belongs to.')
    )
    index = models.PositiveSmallIntegerField(
        _('Index'),
        db_index=True,
        help_text=_('Model the domain structure by positioning this division '
                    'relative to others. 0 is the highest level. Divisions of '
                    'equivalent level  should have an equal value.')
    )
    name = models.CharField(
        _('Name'),
        db_index=True,
        max_length=255,
        help_text=_('The name of this division. Divisions under the same Domain'
                    ' must be named uniquely.')
    )
    budgeting = models.BooleanField(
        _('Budgeting'),
        db_index=True,
        default=False,
        help_text=_('Indicates whether entities that belong to this division '
                    'are budgeting entities.')
    )

    @property
    def entity_count(self):
        return Entity.objects.related_map().filter(division=self).count()

    class Meta:
        ordering = ['index', 'name']
        verbose_name = _('division')
        verbose_name_plural = _('divisions')
        unique_together = (
            ('name', 'domain'),
        )

    def __unicode__(self):
        return self.name


class EntityManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map_min(self):
        return self.select_related()

    def related_map(self):
        return self.select_related().prefetch_related('sheets', 'parent')


class Entity(TimeStampedModel, ClassMethodMixin):
    """Entity describes the actual units in our organizational structure."""

    objects = EntityManager()

    division = models.ForeignKey(
        Division,
        related_name='entities',
        help_text=_('The division that this entity belongs to.')
    )
    name = models.CharField(
        _('Name'),
        db_index=True,
        max_length=255,
        help_text=_('The name of this entity.')
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        help_text=_('A short text for this entity, useful as an overview.')
    )
    code = models.CharField(
        _('Code'),
        max_length=25,
        blank=True,
        help_text=_('An identifying code for this entity.')
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children'
    )
    slug = AutoSlugField(
        db_index=True,
        populate_from='name',
        unique=True
    )

    @property
    def ultimate_parent(self):
        """Returns the ultimate parent of this object. If none, returns self."""

        return get_ultimate_parent(self.parent)

    @property
    def siblings(self):
        """Returns all other entities in the same division."""

        return Entity.objects.related_map().filter(division=self.division).\
            exclude(id=self.id)

    @property
    def periods(self):
        return [sheet.period for sheet in self.sheets.all()]

    class Meta:
        ordering = ('division__domain', 'division__index', 'name')
        verbose_name = _('entity')
        verbose_name_plural = _('entities')
        unique_together = (
            ('name', 'parent', 'division'),
        )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'entity_detail', [self.slug]
