from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from oauth2_provider.models import AbstractApplication
from autoslug import AutoSlugField
from openbudget.apps.accounts.models import Account
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel, ClassMethodMixin


class ProjectManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map(self):
        return self.select_related()


class Project(AbstractApplication, TimeStampedModel, UUIDModel, ClassMethodMixin):
    """API Project object, comprised of initial data + some meta data."""

    LABEL_CHOICES = (
        ('public', _('For the General Public')),
        ('developers', _('For Developers'))
    )

    objects = ProjectManager()

    author = models.ForeignKey(
        Account,
        related_name='author_projects'
    )
    description = models.TextField(
        _('Description'),
        help_text=_('Provide a short description of this project')
    )
    label = models.CharField(
        max_length=50,
        choices=LABEL_CHOICES,
        default=LABEL_CHOICES[0][0],
        help_text=_('Set your preferred language for the app')
    )
    featured = models.BooleanField(
        _('Featured'),
        default=False,
    )
    screenshot = models.URLField(
        _('Screenshot'),
        blank=True,
        null=True,
        help_text=_('A screenshot for this visualization')
    )
    slug = AutoSlugField(
        db_index=True,
        populate_from='name',
        unique=True
    )
    config = JSONField(
        _('Data and configuration'),
        blank=True,
        null=True,
        help_text=_('JSON serialized configuration object of the visualization.')
    )

    @models.permalink
    def get_absolute_url(self):
        return 'project_detail', [self.slug]

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class StateManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map(self):
        return self.select_related()


class State(TimeStampedModel, UUIDModel, ClassMethodMixin):
    """State objects describe saved states of specific projects."""

    objects = StateManager()

    project = models.ForeignKey(
        Project,
        related_name='states'
    )
    author = models.ForeignKey(
        Account,
        related_name='saved_states'
    )
    screenshot = models.URLField(
        _('Screenshot'),
        blank=True,
        null=True,
        help_text=_('A screenshot for this state')
    )
    config = JSONField(
        _('Data and configuration'),
        blank=True,
        null=True,
        help_text=_('JSON serialized configuration object of the state.')
    )

    @models.permalink
    def get_absolute_url(self):
        return 'state-detail', [self.uuid]

    def __unicode__(self):
        return self.project.name + u'state: ' + unicode(self.last_modified)

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
