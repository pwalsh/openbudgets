from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from openbudget.apps.entities.models import DomainDivision, Entity
from openbudget.apps.sources.models import DataSource
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel, PeriodStartModel, PeriodicModel


class Annotation(UUIDModel, TimeStampedModel):
    user = models.OneToOneField(
        User
    )
    note = models.TextField(
        _('note'),
        blank=True,
        help_text=_('This note.')
    )
    content_type = models.ForeignKey(
        ContentType,
        editable=False
    )
    object_id = models.PositiveIntegerField(
        editable=False
    )
    content_object = generic.GenericForeignKey(
        'content_type', 'object_id',
    )

    class Meta:
        ordering = ['user']
        verbose_name = _('Annotation')
        verbose_name_plural = _('Annotations')


class BudgetTemplate(TimeStampedModel, UUIDModel, PeriodStartModel, models.Model):
    """
    The budget template for a given domain division.
    """
    divisions = models.ManyToManyField(
        DomainDivision,
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
        return BudgetTemplateNode.objects.filter(templates=self)

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    class Meta:
        ordering = ['name']
        verbose_name = _('Budget template')
        verbose_name_plural = _('Budget templates')

    @models.permalink
    def get_absolute_url(self):
        return ('budget_template_detail', [self.uuid])

    def __unicode__(self):
        return self.name


class BudgetTemplateNode(TimeStampedModel, UUIDModel):
    """The individual nodes in a budget template"""

    NODE_DIRECTIONS = (
        ('REVENUE', _('REVENUE')),
        ('EXPENDITURE', _('EXPENDITURE'))
    )

    templates = models.ManyToManyField(
        BudgetTemplate,
        through='BudgetTemplateNodeRelation',
        related_name='node_set'
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
        related_name='children'
    )
    # forwards = models.ManyToManyField(
    #     'self',
    #     null=True,
    #     blank=True,
    #     symmetrical=False,
    #     related_name='pasts'
    # )
    backwards = models.ManyToManyField(
        'self',
        null=True,
        blank=True,
        symmetrical=False,
        related_name='forwards'
    )
    direction = models.CharField(
        _('REVENUE/EXPENDITURE'),
        max_length=15,
        choices=NODE_DIRECTIONS,
        help_text=_('Indicates whether this node is for revenue or expenditure')
    )
    #TODO: validate that never points to itself
    #TODO: validate that it always points to the opposite `direction`
    inverse = models.ManyToManyField(
        'self',
        symmetrical=True,
        null=True,
        blank=True,
        help_text=_('Describe for this entry.')
    )

    @property
    def budget_items(self):
        return BudgetItem.objects.filter(node=self)

    @property
    def actual_items(self):
        return ActualItem.objects.filter(node=self)

    @property
    def past(self):
        nodes = list(self.backwards.all())
        if len(nodes):
            for node in nodes:
                nodes += node.past
        return nodes

    @property
    def future(self):
        nodes = list(self.forwards.all())
        if len(nodes):
            for node in nodes:
                nodes += node.future
        return nodes

    @property
    def with_past(self):
        return [self] + self.past

    @property
    def with_future(self):
        return [self] + self.future

    class Meta:
        ordering = ['name']
        verbose_name = _('Budget template node')
        verbose_name_plural = _('Budget template nodes')
        unique_together = (
            ('code', 'parent') # and name?
        )

    @models.permalink
    def get_absolute_url(self):
        return ('budget_template_node', [self.uuid])

    def __unicode__(self):
        return self.code


class BudgetTemplateNodeRelation(models.Model):
    """A relation between a node and a template"""

    template = models.ForeignKey(
        BudgetTemplate
    )
    node = models.ForeignKey(
        BudgetTemplateNode
    )

    class Meta:
        ordering = ['template__name', 'node__name']
        verbose_name = _('Budget Template/Node Relation')
        verbose_name = _('Budget Template/Node Relations')
        unique_together = (
            ('node', 'template')
        )

    def __unicode__(self):
        return '%s -> %s' % (self.template, self.node)


class Sheet(PeriodicModel, TimeStampedModel, UUIDModel):
    """An abstract class for common Budget and Actual data"""


    entity = models.ForeignKey(
        Entity,
    )
    template = models.ForeignKey(
        BudgetTemplate,
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
        Comment,
        object_id_field="object_pk"
    )

    @property
    def total(self):
        tmp = [item.amount for item in self.item_set.all()]
        value = sum(tmp)
        return value

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    class Meta:
        abstract = True
        ordering = ['entity']


class Budget(Sheet):
    """Budget for the given entity and period"""

    @property
    def actuals(self):
       return Actual.objects.filter(entity=self.entity, period_start=self.period_start, period_end=self.period_end)

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
        return self.__class__.__name__ + ' for ' + self.entity.name \
            + ': ' + unicode(self.period_start) + ' - ' + \
            unicode(self.period_end)


class Actual(Sheet):
    """Actual for the given entity and period"""

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
    def budgets(self):
        return Budget.objects.filter(entity=self.entity, period_start=self.period_start, period_end=self.period_end)

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
        return self.__class__.__name__ + ' for ' + self.entity.name \
            + ': ' + unicode(self.period_start) + ' - ' + \
            unicode(self.period_end)


class SheetItem(TimeStampedModel, UUIDModel):
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
        help_text=_('The amount of this entry. The node determines REVENUE or EXPENDITURE')
    )
    discussion = generic.GenericRelation(
        Comment,
        object_id_field="object_pk"
    )
    annotation = generic.GenericRelation(
        Annotation,
        object_id_field="object_pk"
    )

    @property
    def name(self):
        value = self.node.name
        return value

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    class Meta:
        abstract = True
        ordering = ['node']


class BudgetItem(SheetItem):
    """Describes a single item in a budget"""

    budget = models.ForeignKey(
        Budget,
        related_name='item_set'
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
        Actual,
        related_name='item_set'
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
