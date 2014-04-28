from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from openbudgets.commons.mixins import models as mixins
from openbudgets.commons.utilities import get_media_file_path
from uuidfield import UUIDField


class AbstractDataSource(mixins.UUIDPKMixin, mixins.TimeStampMixin,
                         mixins.ClassMethodMixin):

    """Describes an original source of data.

    All data in the system should declare a data source.
    So, this DataSource model should be generically related
    to any model that stores data.
    """

    class Meta:
        abstract = True

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)ss',)

    name = models.CharField(
        _('Source Name'),
        max_length=255,
        help_text=_('The name of this data source'),)

    data = models.FileField(
        _('Source data file'),
        upload_to=get_media_file_path,
        blank=True,
        help_text=_('The source file.'),)

    url = models.URLField(
        _('Source URL'),
        blank=True,
        help_text=_('The URL the data was retrieved from'),)

    retrieval_date = models.DateField(
        _('Data retrieval date'),
        help_text=_('The date this data was retrieved from the source'),)

    notes = models.TextField(
        _('Notes'),
        help_text=_('Write any additional notes about the sourcing of this '
                    'dataset'),)

    content_type = models.ForeignKey(
        ContentType,
        editable=False,)

    object_id = UUIDField(
        editable=False,)

    content_object = generic.GenericForeignKey(
        'content_type', 'object_id',)

    def __unicode__(self):
        return self.name


class ReferenceSource(AbstractDataSource):

    class Meta:
        ordering = ['last_modified', 'name']
        verbose_name = _('Reference source')
        verbose_name_plural = _('Reference sources')

    def get_absolute_url(self):
        return reverse('reference_source_detail', [self.pk])


class AuxSource(AbstractDataSource):

    class Meta:
        ordering = ['last_modified', 'name']
        verbose_name = _('Auxilliary source')
        verbose_name_plural = _('Auxilliary sources')

    def get_absolute_url(self):
        return reverse('aux_source_detail', [self.pk])

