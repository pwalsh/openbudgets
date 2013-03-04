from django.db import models
from django.db.models import Q
from django.db.models.loading import get_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from autoslug import AutoSlugField
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel
from openbudget.commons.utilities import get_ultimate_parent


GEOPOL_TYPE_CHOICES = (
    ('state', 'State'),
    ('muni', 'Municipality')
)


class GeoPoliticalEntity(TimeStampedModel, UUIDModel, models.Model):
    """Describes a State, municipality, or other geopolitical entity"""

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('The name of this Geopolitical entity.')
    )
    description = models.TextField(
        _('Entry description'),
        blank=True,
        help_text=_('Describe.')
    )
    slug = AutoSlugField(
        populate_from='name',
        unique=True
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text=_('The official abbreviated code for this Geopolitical entity.')
    )
    is_type = models.CharField(
        max_length=20,
        choices=GEOPOL_TYPE_CHOICES,
        help_text=_('Declare the type of entity this geopol is from the available choices.')
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True
    )
    discussion = generic.GenericRelation(
        Comment,
        object_id_field="object_pk"
    )

    @property
    def state(self):
        """Returns the State (Country) for this entity.

        Gets the state for this object with this logic:

        * if is_type State, then return self
        * if is_type is not State, then recurse
        parents until encounter the ultimate parent, and
        ensure that the ultimate parent is_type State
        before returning it.
        """
        value = None
        if self.is_type == 'state':
            value = self
        else:
            ultimate_parent = get_ultimate_parent(self.parent)
            if ultimate_parent.is_type == 'state':
                value = ultimate_parent
        return value

    @property
    def munis(self):
        """Returns a list of related muni objects.

        Gets the munis for this object with this logic:

        * if is_type State, get all the State's munis
        * if is_type Muni, get all sibling munis.
        * otherwise, return None.
        """
        value = None
        excludes = []
        if self.is_type == 'muni':
            value = self.state.munis.exclude(pk=self.pk)

        if self.is_type == 'state':
            tmp = GeoPoliticalEntity.objects.filter(is_type='muni')
            for obj in tmp:
                if obj.state != self:
                    excludes.append(obj.pk)
            value = tmp.exclude(pk__in=excludes)
        return value

    @property
    def budgets(self):
        Budget = get_model('budgets', 'Budget')
        value = Budget.objects.filter(geopol=self)
        return value

    @property
    def actuals(self):
        Actual = get_model('budgets', 'Actual')
        value = Actual.objects.filter(geopol=self)
        return value

    # TODO: see my notes in govts.views
    # want to build better slugs for SEO (bots and humans)
    #@property
    #def extended_slug(self):
    #    return unicode(self.state.slug) + ',' + unicode(self.slug)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('geopol_detail', [self.slug])

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    # TODO: clean method
    # 1. State CAN'T have parent
    # 2. Muni MUST have parent

    class Meta:
        ordering = ['name']
        verbose_name = _('Geopolitical entity')
        verbose_name_plural = _('Geopolitical entities')
