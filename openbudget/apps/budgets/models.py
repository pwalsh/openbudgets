from __future__ import division
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from openbudget.apps.entities.models import DomainDivision, Entity
from openbudget.apps.sources.models import ReferenceSource, AuxSource
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel, PeriodStartModel, PeriodicModel


PATH_SEPARATOR = '|'


class BudgetTemplate(TimeStampedModel, UUIDModel, PeriodStartModel):
    """The budget template for a given domain division.

    """

    divisions = models.ManyToManyField(
        DomainDivision,
    )

    name = models.CharField(
        max_length=255,
        help_text=_('The name of this budget template.')
    )

    description = models.TextField(
        _('Entry description'),
        blank=True,
        help_text=_('Describe for this entry.')
    )

    referencesources = generic.GenericRelation(
        ReferenceSource
    )

    auxsources = generic.GenericRelation(
        AuxSource
    )

    @property
    def nodes(self):
        return BudgetTemplateNode.objects.filter(templates=self)

    @property
    def has_budgets(self):
        return bool(self.budgets.count())

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    @models.permalink
    def get_absolute_url(self):
        return ('budget_template_detail', [self.uuid])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Budget template')
        verbose_name_plural = _('Budget templates')


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

    path = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Codes path to root.')
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

    referencesources = generic.GenericRelation(
        ReferenceSource
    )

    auxsources = generic.GenericRelation(
        AuxSource
    )

    def save(self, *args, **kwargs):
        # only handle creation of a new instance for now
        if not self.id:
            # set the `path` property if not set and needed
            if not self.path:
                self.path = PATH_SEPARATOR.join(self._path_to_root)

        #TODO: perhaps handle updates too?

        return super(BudgetTemplateNode, self).save(*args, **kwargs)

    @property
    def _path_to_root(self):
        path = [self.code]
        if self.parent:
            parent_path = self.parent._path_to_root
            if parent_path:
                path = path + parent_path

        return path

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

    @property
    def timeline(self):
        return self.with_past + self.future

    @models.permalink
    def get_absolute_url(self):
        return ('budget_template_node', [self.uuid])

    def __unicode__(self):
        return self.code

    class Meta:
        ordering = ['name']
        verbose_name = _('Budget template node')
        verbose_name_plural = _('Budget template nodes')


class BudgetTemplateNodeRelationManager(models.Manager):
    def has_same_node(self, node, template):
        return self.filter(
            node__code=node.code,
            node__name=node.name,
            node__parent=node.parent,
            template=template
        ).count()


class BudgetTemplateNodeRelation(models.Model):
    """A relation between a node and a template"""

    objects = BudgetTemplateNodeRelationManager()

    template = models.ForeignKey(
        BudgetTemplate
    )

    node = models.ForeignKey(
        BudgetTemplateNode
    )

    def validate_unique(self, exclude=None):
        node = self.node
        super(BudgetTemplateNodeRelation, self).validate_unique(exclude)
        if not bool(self.__class__.objects.has_same_node(node, self.template)):
            raise ValidationError(
                _('Node with name: %s; code: %s; parent: %s; already exists in template: %s' %
                  (node.name, node.code, node.parent, self.template))
            )

    def __unicode__(self):
        return '%s -> %s' % (self.template, self.node)

    class Meta:
        ordering = ['template__name', 'node__name']
        verbose_name = _('Budget Template/Node Relation')
        verbose_name = _('Budget Template/Node Relations')
        unique_together = (
            ('node', 'template')
        )


class Sheet(PeriodicModel, TimeStampedModel, UUIDModel):
    """An abstract class for common Budget and Actual data"""

    entity = models.ForeignKey(
        Entity,
        related_name='%(class)s'
    )

    template = models.ForeignKey(
        BudgetTemplate,
        related_name='%(class)s'
    )

    description = models.TextField(
        _('Budget description'),
        blank=True,
        help_text=_('Descriptive text for this %(class)s')
    )

    referencesources = generic.GenericRelation(
        ReferenceSource
    )

    auxsources = generic.GenericRelation(
        AuxSource
    )

    @property
    def total(self):
        tmp = [item.amount for item in self.items.all()]
        value = sum(tmp)
        return value

    @property
    def item_count(self):
        value = self.items.all().count()
        return value

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    def __unicode__(self):
        return unicode(self.period) + ' ' + self.__class__.__name__ + ' for ' + self.entity.name

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

    @models.permalink
    def get_absolute_url(self):
        return ('budget_detail', [self.uuid])

    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')


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

    @models.permalink
    def get_absolute_url(self):
        return ('actual_detail', [self.uuid])

    class Meta:
        verbose_name = _('Actual')
        verbose_name_plural = _('Actuals')


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

    referencesources = generic.GenericRelation(
        ReferenceSource
    )

    auxsources = generic.GenericRelation(
        AuxSource
    )

    comments = generic.GenericRelation(
        Comment,
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


class BudgetItemManager(models.Manager):
    def timeline(self, node_uuid, entity_uuid):
        try:
            node = BudgetTemplateNode.objects.get(uuid=node_uuid)
        except BudgetTemplateNode.DoesNotExist as e:
            raise e
        return BudgetItem.objects.filter(node__in=node.timeline, budget__entity__uuid=entity_uuid)


class BudgetItem(SheetItem):
    """Describes a single item in a budget"""

    objects = BudgetItemManager()

    budget = models.ForeignKey(
        Budget,
        related_name='items'
    )

    @models.permalink
    def get_absolute_url(self):
        return ('budget_item_detail', [self.uuid])

    def __unicode__(self):
        return self.node.code

    class Meta:
        verbose_name = _('Budget item')
        verbose_name_plural = _('Budget items')


class ActualItemManager(models.Manager):
    def timeline(self, node_uuid, entity_uuid):
        try:
            node = BudgetTemplateNode.objects.get(uuid=node_uuid)
        except BudgetTemplateNode.DoesNotExist as e:
            raise e
        return ActualItem.objects.filter(node__in=node.timeline, actual__entity__uuid=entity_uuid)


class ActualItem(SheetItem):
    """Describes a single item in an actual"""

    objects = ActualItemManager()

    actual = models.ForeignKey(
        Actual,
        related_name='items'
    )

    @models.permalink
    def get_absolute_url(self):
        return ('actual_item_detail', [self.uuid])

    def __unicode__(self):
        return self.node.code

    class Meta:
        verbose_name = _('Actual item')
        verbose_name_plural = _('Actual items')
