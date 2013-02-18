from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from omuni.commons.data import OBJECT_STATES
from omuni.commons.mixins.models import TimeStampedModel


class Page(TimeStampedModel, models.Model):

    status = models.IntegerField(
        _('Publication status'),
        choices=OBJECT_STATES,
        default=1,
        help_text=_('Determines whether the page is publically accessible or not.')
    )
    title = models.CharField(
        _('Page title'),
        max_length=70,
        help_text=_('The main heading for your page.')
    )
    slug = AutoSlugField(
        populate_from='title',
        unique=True
    )
    content = models.TextField(
        _('Content'),
        help_text=_('The main content for this page.')
    )
    index = models.IntegerField(
        _('Index'),
        default=0,
        help_text=_('A number used to order pages in indexes, as an alternative to date-based ordering.')
    )
    in_nav = models.BooleanField(
        _('Show in navigation'),
        default=True,
        help_text=_('A hook to control whether the page will be displayed in main navigation lists.')
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True
    )

    @models.permalink
    def get_absolute_url(self):
        return ('page', [self.slug])

    def __unicode__(self):
        return self.slug

    class Meta:
        ordering = ['slug', 'last_modified', 'index']
        verbose_name = _('page')
        verbose_name_plural = _('pages')
