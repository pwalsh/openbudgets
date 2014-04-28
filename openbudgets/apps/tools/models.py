from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from oauth2_provider.models import AbstractApplication
from autoslug import AutoSlugField
from openbudgets.apps.accounts.models import Account
from openbudgets.commons.mixins import models as mixins


class ToolManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map(self):
        return self.select_related()


class Tool(mixins.UUIDPKMixin, AbstractApplication, mixins.TimeStampMixin,
           mixins.ClassMethodMixin):

    """Tool object, comprised of initial data + some meta data."""

    class Meta:
        verbose_name = _('tool')
        verbose_name_plural = _('tools')

    LABEL_CHOICES = (('public', _('For the General Public')),
                     ('developers', _('For Developers')),)

    objects = ToolManager()

    author = models.ForeignKey(
        Account,
        related_name='author_tools',)

    description = models.TextField(
        _('Description'),
        help_text=_('Provide a short description of this tool'),)

    label = models.CharField(
        max_length=50,
        choices=LABEL_CHOICES,
        default=LABEL_CHOICES[0][0],
        help_text=_('The type of tool'),)

    featured = models.BooleanField(
        _('Featured'),
        default=False,)

    screenshot = models.URLField(
        _('Screenshot'),
        blank=True,
        null=True,
        help_text=_('A screenshot for this tool'),)

    slug = AutoSlugField(
        db_index=True,
        populate_from='name',
        unique=True,)

    config = JSONField(
        _('Data and configuration'),
        blank=True,
        null=True,
        help_text=_('JSON serialized configuration object of the tool.'),)

    def get_absolute_url(self):
        return reverse('tool_detail', [self.slug])

    def __unicode__(self):
        return self.name


class StateManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map(self):
        return self.select_related()


class State(mixins.UUIDPKMixin, mixins.TimeStampMixin, mixins.ClassMethodMixin):

    """State objects describe saved states of specific projects."""

    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')

    objects = StateManager()

    tool = models.ForeignKey(
        Tool,
        related_name='states',)

    author = models.ForeignKey(
        Account,
        related_name='saved_states',)

    screenshot = models.URLField(
        _('Screenshot'),
        blank=True,
        null=True,
        help_text=_('A screenshot for this state'),)

    config = JSONField(
        _('Data and configuration'),
        blank=True,
        null=True,
        help_text=_('JSON serialized configuration object of the state.'),)

    def get_absolute_url(self):
        return reverse('state_detail', [self.project.slug, self.uuid])

    def __unicode__(self):
        return self.tool.name + u'state: ' + unicode(self.last_modified)
