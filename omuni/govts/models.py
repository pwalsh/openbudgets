from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.loading import get_model
from autoslug import AutoSlugField


GEOPOL_TYPE_CHOICES = (
    ('state', 'state'),
    ('muni', 'muni')
)


class GeoPoliticalEntity(models.Model):
    """Describes a State, municipality, or other geopolitical entity"""

    name = models.CharField(
        max_length=255,
        help_text=_('The name of this Geopolitical entity.')
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
        choices=GEOPOL_TYPE_CHOICES
    )
    under = models.ForeignKey(
        'self',
        null=True,
        blank=True
    )

    @property
    def budgets(self):
        Budget = get_model('budgets', 'Budget')
        value = Budget.objects.filter(geopol=self)
        return value

    @property
    def direct_children(self):
        value = GeoPoliticalEntity.objects.filter(under=self)
        return value

    # @property: ultimate parent (country)

    # clean method: if type_is is state, then part_of must be null
    # and blank. and other related checks for toher situations.

    class Meta:
        ordering = ['name']
        verbose_name = _('Geopolitical entity')
        verbose_name_plural = _('Geopolitical entities')

    @models.permalink
    def get_absolute_url(self):
        return ('geopol_detail', [self.slug])

    def __unicode__(self):
        return self.name
