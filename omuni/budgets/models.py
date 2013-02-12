from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from uuidfield import UUIDField
from omuni.govts.models import GeoPoliticalEntity, GEOPOL_TYPE_CHOICES
from omuni.commons.models import DataSource
from omuni.commons.mixins.models import TimeStampedModel


NODE_DIRECTIONS = (
    (1, _('income')), (2, _('expense'))
)


class BudgetTemplate(TimeStampedModel, models.Model):
    """The budget template for a given geopolitical entity"""

    uuid = UUIDField(
        auto=True
    )
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


class BudgetTemplateNode(TimeStampedModel, models.Model):
    """The individual nodes in a budget template"""

    uuid = UUIDField(
        auto=True
    )
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
    def items(self):
        return BudgetItem.objects.filter(code=self)

    class Meta:
        ordering = ['name']
        verbose_name = _('Budget template node')
        verbose_name_plural = _('Budget template nodes')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_template_node', [self.uuid])

    def __unicode__(self):
        return self.code


class Budget(TimeStampedModel, models.Model):
    """A budget for the given year and geopolitical entity"""

    uuid = UUIDField(
        auto=True
    )
    geopol = models.ForeignKey(
        GeoPoliticalEntity,
    )
    period_start = models.DateField(
        _('Period start'),
        help_text=_('The start date for this budget')
    )
    period_end = models.DateField(
        _('Period end'),
        help_text=_('The end date for this budget')
    )
    description = models.TextField(
        _('Budget description'),
        blank=True,
        help_text=_('Text for this budget.')
    )
    sources = generic.GenericRelation(
        DataSource
    )

    @property
    def items(self):
        value = BudgetItem.objects.filter(budget=self)
        return value

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

    class Meta:
        ordering = ['geopol']
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_detail', [self.uuid])

    def __unicode__(self):
        return self.geopol.name + ': ' + unicode(self.period_start) + ' - ' + unicode(self.period_end)


class BudgetItem(TimeStampedModel, models.Model):
    """Describes the minimal attributes of a single item in a budget"""
    uuid = UUIDField(
        auto=True
    )
    budget = models.ForeignKey(
        Budget
    )
    node = models.ForeignKey(
        BudgetTemplateNode
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
        ordering = ['node']
        verbose_name = _('Budget item')
        verbose_name_plural = _('Budget items')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_item_detail', [self.uuid])

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
