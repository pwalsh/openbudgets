from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.loading import get_model
from django.contrib.contenttypes import generic
from autoslug import AutoSlugField
from omuni.commons.mixins.models import TimeStampedModel, UUIDModel
from omuni.interactions.models import IComment


GEOPOL_TYPE_CHOICES = (
    ('state', 'state'),
    ('muni', 'muni')
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
    type_is = models.CharField(
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
        IComment,
        object_id_field="object_pk"
    )

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

    @property
    def children(self):
        return GeoPoliticalEntity.objects.filter(parent=self)

    @property
    def descendants(self):
        children = self.children
        result = [] + list(children)
        for node in children:
            result += node.descendants
        return result

    # @property: root (country)
    # TODO: some work in the clean method of the model
    # clean method: if type_is is state, then part_of must be null
    # and blank. and other related checks for toher situations.

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    class Meta:
        ordering = ['name']
        verbose_name = _('Geopolitical entity')
        verbose_name_plural = _('Geopolitical entities')

    @models.permalink
    def get_absolute_url(self):
        return ('geopol_detail', [self.slug])

    def __unicode__(self):
        return self.name
