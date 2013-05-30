from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from provider.oauth2.models import Client
from openbudget.settings import base as settings
from openbudget.apps.accounts.models import Account
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel, ClassMethodMixin


class Project(TimeStampedModel, UUIDModel, ClassMethodMixin):
    """
    Visualization state object comprised of configuration, data input and some meta data.
    """
    auth = models.OneToOneField(
        Client,
    )
    owner = models.ForeignKey(
        Account,
        related_name='owner_projects'
    )
    author = models.ForeignKey(
        Account,
        related_name='author_projects'
    )
    name = models.CharField(
        _('Name'),
        max_length=255,
        help_text=_('The name of this project')
    )
    description = models.TextField(
        _('Description'),
        help_text=_('Provide a short description of this project')
    )
    featured = models.BooleanField(
        _('Featured'),
        default=False,
    )
    preview = models.ImageField(
        _('Preview'),
        # TODO: write a function to customize upload to user directory
        upload_to=settings.MEDIA_ROOT,
        blank=True,
        null=True,
        help_text=_('A preview image for this visualization')
    )
    config = JSONField(
        _('Data and configuration'),
        blank=True,
        null=True,
        help_text=_('JSON serialized configuration object of the visualization.')
    )

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', [self.uuid])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

