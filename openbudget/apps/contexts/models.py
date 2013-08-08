from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from openbudget.apps.entities.models import Entity
from openbudget.commons.mixins.models import PeriodicModel, TimeStampedModel


class ContextManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map(self):
        return self.select_related()


class Context(TimeStampedModel, PeriodicModel):
    """A JSON object with contextual data for the given Entity/Time Period.

    We store contextual data only for the purpose of normalizing comparative
    queries over budget data. Future, or alternate, implementations could take
    contextual data from another source, such as a dedicated API for statistics
    on municipalities, or some other open CBS-type data source.

    No particular keys are required at the data level.

    Currently, Open Budget *expects* to find at least the following keys for use
    on Entity detail pages, and the web API for visualizations:

    * population
    * students
    * ground_surface

    """

    objects = ContextManager()

    entity = models.ForeignKey(
        Entity
    )
    data = JSONField(
        _('Data object'),
        help_text=_('Contextual data as JSON for the Entity/Time Period.')
    )

    # TODO: Enforce some period

    def __unicode__(self):
        return 'Contextual data for {entity} in {period}'.format(
            entity=self.entity.name, period=self.period)
