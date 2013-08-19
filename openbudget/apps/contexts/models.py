from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from openbudget.apps.entities.models import Entity
from openbudget.commons.mixins.models import PeriodicModel, TimeStampedModel


class ContextManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map(self):
        return self.select_related()

    def by_entity(self, entity_id):
        return self.filter(entity=entity_id)

    def latest_of(self, entity_id):
        return self.by_entity(entity_id=entity_id).latest('period_start')


class Context(TimeStampedModel, PeriodicModel):
    """A JSON object with contextual data for the given Entity/Time Period.

    We store contextual data only for the purpose of normalizing comparative
    queries over budget data. Future, or alternate, implementations could take
    contextual data from another source, such as a dedicated API for statistics
    on municipalities, or some other open CBS-type data source.

    No particular keys are required at the data level.

    """

    KEYS = {
        'population': _('Population'),
        'population_male': _('Population (Female)'),
        'population_female': _('Population (Male)'),
        'ground_surface': _('Ground Surface'),
        'students': _('Students'),
        'schools': _('Schools'),
        'gini_index': _('Gini Index'),
        'socioeconomic_index': _('Socio-Economic Index')
    }

    objects = ContextManager()

    entity = models.ForeignKey(
        Entity,
        related_name='contexts'
    )
    data = JSONField(
        _('Data object'),
        help_text=_('Contextual data as JSON for the Entity/Time Period.')
    )

    def __unicode__(self):
        return 'Contextual data for {entity} in {period}'.format(
            entity=self.entity.name, period=self.period)
