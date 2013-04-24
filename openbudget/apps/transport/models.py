from django.db import models
from django.utils.translation import ugettext_lazy as _
from openbudget.commons.mixins.models import TimeStampedModel


class String(TimeStampedModel):
    """"""
    string = models.CharField(
        _('String'),
        max_length=255,
        unique=True,
        help_text=_('A word or some such.')
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='scope_set'
    )

    def __unicode__(self):
        return self.string
