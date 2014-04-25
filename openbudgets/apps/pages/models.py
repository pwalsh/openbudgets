from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from openbudgets.commons.mixins import models as mixins


class Page(mixins.TimeStampMixin, mixins.ClassMethodMixin):

    """Model for simple, generic web pages."""

    STATUS_CHOICES = ((1, 'draft'), (2, 'published'))

    class Meta:
        ordering = ['slug', 'last_modified', 'index']
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    status = models.IntegerField(
        _('Publication status'),
        choices=STATUS_CHOICES,
        default=1,
        help_text=_('Determines whether the page is publically accessible or '
                    'not.'),)

    title = models.CharField(
        _('Page title'),
        max_length=70,
        help_text=_('The main heading for your page.'),)

    slug = AutoSlugField(
        populate_from='title',
        unique=True,)

    content = models.TextField(
        _('Content'),
        help_text=_('The main content for this page.'),)

    index = models.IntegerField(
        _('Index'),
        default=0,
        help_text=_('A number used to order pages in indexes, as an '
                    'alternative to date-based ordering.'),)

    in_nav = models.BooleanField(
        _('Show in navigation'),
        default=True,
        help_text=_('A hook to control whether the page will be displayed in '
                    'main navigation lists.'),)

    parent = models.ForeignKey(
        'self',
        related_name='children',
        blank=True,
        null=True,)

    def get_absolute_url(self):
        return reverse('page', [self.slug])

    def __unicode__(self):
        return self.slug
