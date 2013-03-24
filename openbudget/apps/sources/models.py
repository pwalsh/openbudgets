from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel


class DataSource(TimeStampedModel, UUIDModel):
    """Describes an original source of data.

    All data in the system should declare a data source.
    So, this DataSource model should be generically related
    to any model that stores data.
    """

    name = models.CharField(
        _('Source Name'),
        max_length=255,
        help_text=_('The name of this data source')
    )
    url = models.URLField(
        _('Source URL'),
        blank=True,
        help_text=_('The URL the data was retrieved from')
    )
    retrieval_date = models.DateField(
        _('Data retrieval date'),
        help_text=_('The date this data was retrieved from the source')
    )
    notes = models.TextField(
        _('Notes'),
        help_text=_('Write any additional notes about the sourcing of this dataset')
    )
    content_type = models.ForeignKey(
        ContentType,
        editable=False
    )
    object_id = models.PositiveIntegerField(
        editable=False
    )
    content_object = generic.GenericForeignKey(
        'content_type', 'object_id',
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Data source')
        verbose_name_plural = _('Data sources')

    @models.permalink
    def get_absolute_url(self):
        return ('data_source_detail', [self.uuid])

    def __unicode__(self):
        return self.name
