from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from openbudgets.apps.entities.models import Domain, Entity
from openbudgets.commons.mixins.models import PeriodicMixin, TimeStampedMixin, \
    ClassMethodMixin, UUIDPKMixin


class ContextManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map(self):
        return self.select_related()

    def by_entity(self, entity_id):
        return self.filter(entity=entity_id)

    def latest_of(self, entity_id):
        return self.by_entity(entity_id=entity_id).latest('period_start')


class Context(UUIDPKMixin, TimeStampedMixin, PeriodicMixin, ClassMethodMixin):

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
        related_name='contexts',)

    data = JSONField(
        _('Data object'),
        help_text=_('Contextual data as JSON for the Entity/Time Period.'),)

    def __unicode__(self):
        return 'Contextual data for {entity} in {period}'.format(
            entity=self.entity.name, period=self.period)


class Coefficient(UUIDPKMixin, TimeStampedMixin, PeriodicMixin, ClassMethodMixin):

    """Co-efficient sets for working with nominal monetary values."""

    class Meta:
        ordering = ['domain__name', 'period_start', 'last_modified']
        verbose_name = _('co-efficient')
        verbose_name_plural = _('co-efficients')

    domain = models.ForeignKey(
        Domain,)

    inflation = models.DecimalField(
        _('Inflation'),
        db_index=True,
        max_digits=23,
        decimal_places=20,
        blank=True,
        null=True,
        help_text=_('Inflation co-efficient, where the current year should '
                    'always be 1, and previous years scaled appropriately.'
                    'Use the inflation co-efficient to calculate real values'
                    'from nominal values.'),)

    def __unicode__(self):
        return 'Co-efficient set for {domain} in {period}'.format(
            domain=self.domain.name, period=self.period)
