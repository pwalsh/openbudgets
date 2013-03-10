from django.db import models
from django.db.models import Q
from django.db.models.loading import get_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from mptt.models import MPTTModel, TreeForeignKey
from autoslug import AutoSlugField
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel
from openbudget.commons.utilities import get_ultimate_parent


class Domain(TimeStampedModel, models.Model):
    """Describes the domain for a collection of entities.

    Through the Domain model, we can derive a relational structure for a set of entities.

    We want the domain structure so that we can acheive the
    important goal of comparision across comparable entities,
    and so we can create meta data on the domain as a whole
    from its parts.

    """
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('The name of this entity domain.')
    )

    @property
    def divisions(self):
        value = DomainDivision.objects.filter(domain=self)
        return value

    @property
    def entities(self):
        value = Entity.objects.filter(division__domain=self)
        return value

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('entity domain')
        verbose_name_plural = _('entity domains')


class DomainDivision(TimeStampedModel, models.Model):
    """Describes the administrative division for a domain.

    Each instance is an administrative division of a domain.

    The position of the DomainDivision in the administrative
    structure can be derived from the index attribute. Many
    administrative structures are tree-like, but there are often
    exceptions:
    (eg: muni > sub-division > division for Tel Aviv and Jerusalem)

    And seemingly arbitrary designations (in terms of modeling data)
    at the same "level" of a tree:
    (eg: city, local and regional munis in Israel)

    Also, not all Admnistrative levels present budgets:
    (eg: divisons and sb-divisions in Israeli government)
    Hence the has_budgets flag.

    """
    domain = models.ForeignKey(
        Domain
    )
    index = models.PositiveSmallIntegerField(
        _('Index'),
        help_text=_('Position this division in relation to others')
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('The name of this division')
    )
    has_budgets = models.BooleanField(
        _('has budgets'),
        default=False,
        help_text=_('Must be true if this division directly presents budgets')
    )

    @property
    def count(self):
        value = Entity.objects.filter(division=self).count()
        return value

    @property
    def entities(self):
        value = Entity.objects.filter(division=self)
        return value

    def __unicode__(self):
        return self.domain.name + ' > ' + self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('domain division')
        verbose_name_plural = _('domain divisions')


class Entity(MPTTModel, TimeStampedModel, UUIDModel, models.Model):
    """Describes an entity in a domain.


    """
    division = models.ForeignKey(
        DomainDivision
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('The name of this entity')
    )
    description = models.TextField(
        _('Entry description'),
        blank=True,
        help_text=_('Describe.')
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        help_text=_('The official abbreviated code for this entity.')
    )
    discussion = generic.GenericRelation(
        Comment,
        object_id_field="object_pk"
    )
    # TODO: parent choices conditional on division choice?
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children'
    )
    slug = AutoSlugField(
        populate_from='name',
        unique=True
    )

    @property
    def ultimate_parent(self):
        """Returns the ultimate parent entity for this entity.

        Gets the ultimate parent with this logic:

        * if divison.index is 0, then return self
        * if divison.index is not 0, then recurse
        parents until encounter the ultimate parent
        * and ensure that the ultimate parent's
        divison.index is 0 before returning it.
        """
        value = None
        if self.division.index == 0:
            value = self
        else:
            ultimate_parent = get_ultimate_parent(self.parent)
            #if ultimate_parent.divison.index == 0:
            value = ultimate_parent
        return value

    @property
    def related_entities(self):
        """Returns all related entities for this entity.

        Relation is determined by Domain, and whether the entity
        is a budgeting entity.
 
        """
        value = Entity.objects.filter(division__domain=self.division.domain, division__has_budgets=True).exclude(id=self.id)
        return value

    @property
    def budgets(self):
        Budget = get_model('budgets', 'Budget')
        value = Budget.objects.filter(entity=self)
        return value

    @property
    def actuals(self):
        Actual = get_model('budgets', 'Actual')
        value = Actual.objects.filter(entity=self)
        return value

    # TODO: see my notes in entities.views
    # want to build better slugs for SEO (bots and humans)
    #@property
    #def extended_slug(self):
    #    return unicode(self.state.slug) + ',' + unicode(self.slug)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('entity_detail', [self.slug])

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    # TODO: clean method
    # 1. divison.index of 0 CAN'T have parent
    # 2. other division.index values MUST have parent

    class Meta:
        ordering = ['name']
        verbose_name = _('entity')
        verbose_name_plural = _('entities')
