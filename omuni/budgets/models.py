from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuidfield import UUIDField
from omuni.govts.models import GeoPoliticalEntity, GEOPOL_TYPE_CHOICES


BUDGET_YEAR_CHOICES = (
    (year, year) for year in range(1948, 2015)
)


class Budget(models.Model):
    """A budget for the given year and geopolitical entity"""

    uuid = UUIDField(
        auto=True
    )
    geopol = models.ForeignKey(
        GeoPoliticalEntity,
    )
    year = models.PositiveIntegerField(
        choices=BUDGET_YEAR_CHOICES
    )
    description = models.TextField(
        _('Budget description'),
        blank=True,
        help_text=_('Text for this budget.')
    )

    # @property:
    # A method which the budget classification type for the given
    # geopol, and builds a classification structure from the
    # available BudgetResource instances for this Budget

    # @property: total $
    pass


class BudgetClassificationMap(models.Model):
    """The budget classification system for the given geopolitical entity"""

    uuid = UUIDField(
        auto=True
    )
    geopol = models.ForeignKey(
        # must be top level (country) only
        GeoPoliticalEntity,
    )
    target = models.CharField(
        max_length=20,
        choices=GEOPOL_TYPE_CHOICES
    )
    name = models.CharField(
        max_length=255,
        help_text=_('The name of this classification map.')
    )

    @property
    def nodes(self):
        value = BudgetClassificationMapNode.objects.filter(budget_classification_map=self)
        return value

    class Meta:
        ordering = ['name']
        verbose_name = _('Budget classification map')
        verbose_name_plural = _('Budget classification maps')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_classification_map_detail', [self.uuid])

    def __unicode__(self):
        return self.name


class BudgetClassificationMapNode(models.Model):
    """The individual nodes in a budget classification system"""

    uuid = UUIDField(
        auto=True
    )
    budget_classification_map = models.ForeignKey(
        BudgetClassificationMap,
    )
    code = models.CharField(
        max_length=50,
        help_text=_('Code')
    )
    name = models.CharField(
        max_length=255,
        help_text=_('Name')
    )
    description = models.TextField(
        _('Entry description'),
        blank=True,
        help_text=_('Describe for this entry.')
    )
    under = models.ForeignKey(
        'self',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Budget classification map entry')
        verbose_name_plural = _('Budget classification map entries')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_classification_map_entry_detail', [self.uuid])

    def __unicode__(self):
        return self.code


class BudgetItem(models.Model):
    """Describes the minimal attributes of a single item in a budget"""
    uuid = UUIDField(
        auto=True
    )
    budget = models.ForeignKey(
        Budget,
    )
    code = models.ForeignKey(
        BudgetClassificationMapNode,
    )
    explanation = models.TextField(
        _('Item explanation'),
        blank=True,
        help_text=_('Explanation that appears for this entry.')
    )
    amount = models.IntegerField(
        _('Amount'),
        help_text=_('The amount of this entry, plus or minus.')
    )

    class Meta:
        ordering = ['code']
        verbose_name = _('Budget item')
        verbose_name_plural = _('Budget items')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_item_detail', [self.uuid])

    def __unicode__(self):
        return self.code


class BudgetImport(models.Model):
    # save imported CSVs here first
    # process them from here before creating budget object
    # can keep versions of the file too if we need

    # file
    # uploaded by
    # state
    pass
