from __future__ import division
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from omuni.govts.models import GeoPoliticalEntity, GEOPOL_TYPE_CHOICES
from omuni.commons.models import DataSource
from omuni.commons.mixins.models import TimeStampedModel, UUIDModel
from omuni.interactions.models import Remark


NODE_DIRECTIONS = (
    (1, _('income')), (2, _('expense'))
)


class BudgetTemplate(TimeStampedModel, UUIDModel, models.Model):
    """The budget template for a given geopolitical entity"""

    geopol = models.ForeignKey(
        GeoPoliticalEntity,
    )
    target = models.CharField(
        max_length=20,
        choices=GEOPOL_TYPE_CHOICES
    )
    name = models.CharField(
        max_length=255,
        help_text=_('The name of this budget template.')
    )
    sources = generic.GenericRelation(
        DataSource
    )

    @property
    def nodes(self):
        value = BudgetTemplateNode.objects.filter(template=self)
        return value

    # TODO: Clean method that enforces 'geopol' as a top level geopol
    # Meaning, we want this to point to a country only

    class Meta:
        ordering = ['name']
        verbose_name = _('Budget template')
        verbose_name_plural = _('Budget templates')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_template_detail', [self.uuid])

    def __unicode__(self):
        return self.name


class BudgetTemplateNode(TimeStampedModel, UUIDModel, models.Model):
    """The individual nodes in a budget template"""

    template = models.ForeignKey(
        BudgetTemplate,
        null=True,
        blank=True
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
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='node_parent'
    )
    #TODO: in Israeli budget this should be automatically filled in the importer
    direction = models.PositiveSmallIntegerField(
        _('Income/Expense'),
        choices=NODE_DIRECTIONS,
        help_text=_('Determines whether this is an income or expense.')
    )
    #TODO: validate that never points to itself
    #TODO: validate that it points to the opposite `direction`
    # TODO: if setting inverse, always set it on the relation (they should always be the same)
    inverse = models.OneToOneField(
        'self',
        null=True,
        blank=True,
        help_text=_('Describe for this entry.')
    )

    #TODO: implement
    @property
    def root(self):
        pass

    @property
    def budget_items(self):
        return BudgetItem.objects.filter(node=self)

    @property
    def actual_items(self):
        return ActualItem.objects.filter(node=self)


    class Meta:
        ordering = ['name']
        verbose_name = _('Budget template node')
        verbose_name_plural = _('Budget template nodes')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_template_node', [self.uuid])

    def __unicode__(self):
        return self.code


class Sheet(TimeStampedModel, UUIDModel, models.Model):
    """An abstract class for common Budget and Actual data"""

    geopol = models.ForeignKey(
        GeoPoliticalEntity,
    )
    period_start = models.DateField(
        _('Period start'),
        help_text=_('The start date for this %(class)s')
    )
    period_end = models.DateField(
        _('Period end'),
        help_text=_('The end date for this %(class)s')
    )
    description = models.TextField(
        _('Budget description'),
        blank=True,
        help_text=_('Descriptive text for this %(class)s')
    )
    sources = generic.GenericRelation(
        DataSource
    )
    discussion = generic.GenericRelation(
        Remark
    )

    #TODO: implement a shortcut from period_start/end to year
    @property
    def period(self):
        # TODO: Write a smarter method for the general use case
        # naive, just for current purposes
        tmp = self.period_end - self.period_start
        if tmp.days <= 365:
            return self.period_start.year
        else:
            return unicode(self.period_start.year) + ' - ' + self.period_end.year

    @property
    def total(self):
        tmp = [item.amount for item in self.items]
        value = sum(tmp)
        return value

    @classmethod
    def get_class_name(self):
        value = self.__name__.lower()
        return value

    class Meta:
        abstract = True
        ordering = ['geopol']


class Budget(Sheet):
    """Budget for the given geopol and period"""

    @property
    def items(self):
        value = BudgetItem.objects.filter(budget=self)
        return value

    @property
    def actuals(self):
       return Actual.objects.filter(geopol=self.geopol, period_start=self.period_start, period_end=self.period_end)

    @property
    def has_actuals(self):
        # TODO: This is a test POC. need much more robust way
        return bool(len(self.actuals))

    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    @models.permalink
    def get_absolute_url(self):
        return ('actual_detail', [self.uuid])

    def __unicode__(self):
        return self.__class__.__name__ + ' for ' + self.geopol.name \
        + ': ' + unicode(self.period_start) + ' - ' + \
        unicode(self.period_end)


class Actual(Sheet):
    """Actual for the given geopol and period"""

    # Actuals is designed here in parallel to budget for
    # the possible scenarios of:
    # actual report availability, but no budget availability
    # actual report that spans more than one budget, or
    # less than one budget

    # TODO: implement a save method that checks period range,
    # and compares match with budget/actual. Actual periods
    # should smartly map over budget periods, and not fall
    # inconveniently like, an actual for 10 months, but a budget for 12.

    @property
    def items(self):
        value = ActualItem.objects.filter(actual=self)
        return value

    @property
    def budgets(self):
        return Budget.objects.filter(geopol=self.geopol, period_start=self.period_start, period_end=self.period_end)

    @property
    def has_budgets(self):
        # TODO: This is a test POC. need much more robust way
        return bool(len(self.budgets))

    @property
    def variance(self):
        """If this actual has one or more associated budgets in the system, calculate the variance"""
        value = None
        tmp = []
        # TODO: This is a test POC. need much more robust way
        for budget in self.budgets:
            tmp.append(budget.total)

        budget_sum = sum(tmp)
        # We are using python division from future
        value = round(self.total / budget_sum * 100, 2)
        return value

    class Meta:
        verbose_name = _('Actual')
        verbose_name_plural = _('Actuals')

    @models.permalink
    def get_absolute_url(self):
        return ('actual_detail', [self.uuid])

    def __unicode__(self):
        return self.__class__.__name__ + ' for ' + self.geopol.name \
        + ': ' + unicode(self.period_start) + ' - ' + \
        unicode(self.period_end)


class SheetItem(TimeStampedModel, UUIDModel, models.Model):
    """Abstract class for common BudgetItem and ActualItem data"""

    node = models.ForeignKey(
        BudgetTemplateNode
    )
    description = models.TextField(
        _('Item description'),
        blank=True,
        help_text=_('Description that appears for this entry.')
    )
    amount = models.IntegerField(
        _('Amount'),
        help_text=_('The amount of this entry, plus or minus.')
    )
    discussion = generic.GenericRelation(
        Remark
    )

    @property
    def name(self):
        value = self.node.name
        return value

    @classmethod
    def get_class_name(self):
        value = self.__name__.lower()
        return value

    class Meta:
        abstract = True
        ordering = ['node']


class BudgetItem(SheetItem):
    """Describes a single item in a budget"""

    budget = models.ForeignKey(
        Budget
    )

    class Meta:
        verbose_name = _('Budget item')
        verbose_name_plural = _('Budget items')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_item_detail', [self.uuid])

    def __unicode__(self):
        return self.node.code


class ActualItem(SheetItem):
    """Describes a single item in an actual"""

    actual = models.ForeignKey(
        Actual
    )

    class Meta:
        verbose_name = _('Actual item')
        verbose_name_plural = _('Actual items')

    @models.permalink
    def get_absolute_url(self):
        return ('actual_item_detail', [self.uuid])

    def __unicode__(self):
        return self.node.code


class BudgetImport(TimeStampedModel, models.Model):
    # save imported CSVs here first
    # process them from here before creating budget object
    # can keep versions of the file too if we need

    # file
    # uploaded by
    # state
    pass
