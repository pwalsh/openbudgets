from django.db import models
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from omuni.commons.data import OBJECT_STATES


class Page(models.Model):

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
        blank=True,
        help_text=_('The main content for this page.')
    )
    index = models.IntegerField(
        _('Index'),
        default=0,
        help_text=_('A number used to order pages in indexes, as an alternative to date-based ordering.')
    )
    in_nav = models.BooleanField(
        _('Show in navigation'),
        default=1,
        help_text=_('A hook to control whether the page will be displayed in main navigation lists.')
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(
        _('Crated on'),
        auto_now_add=True,
        editable=False,
        help_text=_('The timestamp for when this instance was created.'),
    )
    last_modified = models.DateTimeField(
        _('Last modified'),
        auto_now=True,
        editable=False,
        help_text=_('The timestamp for when this instance was last modified.'),
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
