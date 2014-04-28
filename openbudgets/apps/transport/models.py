from django.db import models
from django.utils.translation import ugettext_lazy as _
from openbudgets.commons.mixins import models as mixins


class String(mixins.TimeStampMixin):

    """Strings and their aliases. Used for keyword mapping in the importer."""

    string = models.CharField(
        _('String'),
        max_length=255,
        unique=True,
        help_text=_('A word or some such.'),)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='scope_set',)

    def __unicode__(self):
        return self.string
