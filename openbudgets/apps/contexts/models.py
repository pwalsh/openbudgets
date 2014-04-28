from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from openbudgets.apps.entities.models import Domain, Entity
from openbudgets.commons.mixins import models as mixins


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


class Context(mixins.UUIDPKMixin, mixins.TimeStampMixin, mixins.PeriodicMixin, mixins.ClassMethodMixin):

    """Contextual data for the given Entity/Time Period.

    We store contextual data only for the purpose of normalizing comparative
    queries over budget data. Future, or alternate, implementations could take
    contextual data from another source, such as a dedicated API for statistics
    on municipalities, or some other open CBS-type data source.

    No particular keys are required at the data level.

    """

    objects = ContextManager()

    entity = models.ForeignKey(
        Entity,
        related_name='contexts',)

    population = models.IntegerField(
        _('population'),
        blank=True,
        null=True,)

    population_male = models.IntegerField(
        _('population male'),
        blank=True,
        null=True,)

    population_female = models.IntegerField(
        _('population female'),
        blank=True,
        null=True,)

    ground_surface = models.IntegerField(
        _('ground surface'),
        blank=True,
        null=True,)

    students = models.IntegerField(
        _('student count'),
        blank=True,
        null=True,)

    schools = models.IntegerField(
        _('school count'),
        blank=True,
        null=True,)

    gini_index = models.DecimalField(
        _('gini index'),
        max_digits=23,
        decimal_places=20,
        blank=True,
        null=True,)

    socioeconomic_index = models.IntegerField(
        _('socioeconomic index'),
        blank=True,
        null=True,)

    def __unicode__(self):
        return 'Contextual data for {entity} in {period}'.format(
            entity=self.entity.name, period=self.period)


class Coefficient(mixins.UUIDPKMixin, mixins.TimeStampMixin,
                  mixins.PeriodicMixin, mixins.ClassMethodMixin):

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
