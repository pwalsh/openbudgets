from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel


class Project(TimeStampedModel, UUIDModel):
    """
    Visualization state object comprised of configuration, data input and some meta data.
    """

    config = JSONField(
        _('Data and configuration'),
        help_text=_('JSON serialized configuration object of the visualization.')
    )

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', [self.uuid])

    def __unicode__(self):
        return '<Project: %s>' % self.uuid

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

