from __future__ import division
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.db.models.signals import m2m_changed
from openbudget.apps.entities.models import Division, Entity
from openbudget.apps.sources.models import ReferenceSource, AuxSource
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel, \
    PeriodStartModel, PeriodicModel, ClassMethodMixin


PATH_SEPARATOR = '|'


class TemplateManager(models.Manager):
    """Exposes the related_map methods for more efficient bulk select queries."""

    def related_map_min(self):
        return self.select_related().prefetch_related('divisions')

    def related_map(self):
        return self.select_related().prefetch_related('divisions', 'nodes',
                                                      'budgets', 'actuals')

    def latest_of(self, entity):
        return self.filter(budgets__entity=entity).latest('period_start')


class Template(TimeStampedModel, UUIDModel, PeriodStartModel, ClassMethodMixin):
    """Templates describe the structure of a Budget or an Actual."""

    objects = TemplateManager()

    divisions = models.ManyToManyField(
        Division,
    )
    name = models.CharField(
        _('Name'),
        db_index=True,
        max_length=255,
        help_text=_('The name of this template.')
    )
    description = models.TextField(
        _('Description'),
        db_index=True,
        blank=True,
        help_text=_('An overview text for this template.')
    )

    referencesources = generic.GenericRelation(
        ReferenceSource
    )
    auxsources = generic.GenericRelation(
        AuxSource
    )

    @property
    def has_budgets(self):
        return bool(self.budgets.count())

    class Meta:
        ordering = ['name']
        verbose_name = _('template')
        verbose_name_plural = _('templates')

    @models.permalink
    def get_absolute_url(self):
        return 'template_detail', [self.uuid]

    def __unicode__(self):
        return self.name


class TemplateNodeManager(models.Manager):
    """Exposes the related_map methods for more efficient bulk select queries."""

    def related_map_min(self):
        return self.prefetch_related('parent', 'children')

    def related_map(self):
        return self.prefetch_related('parent', 'children', 'templates',
                                     'inverse', 'backwards')


class TemplateNode(TimeStampedModel, UUIDModel):
    """The nodes that make up a template."""

    DIRECTIONS = (
        ('REVENUE', _('REVENUE')),
        ('EXPENDITURE', _('EXPENDITURE'))
    )

    objects = TemplateNodeManager()

    templates = models.ManyToManyField(
        Template,
        through='TemplateNodeRelation',
        related_name='nodes'
    )
    name = models.CharField(
        _('Name'),
        db_index=True,
        max_length=255,
        help_text=_('The name of this template node.')
    )
    description = models.TextField(
        _('Entry description'),
        blank=True,
        help_text=_('A descriptive text for this template node.')
    )
    code = models.CharField(
        _('Code'),
        db_index=True,
        max_length=50,
        help_text=_('An identifying code for this template node.')
    )
    direction = models.CharField(
        _('REVENUE/EXPENDITURE'),
        db_index=True,
        max_length=15,
        choices=DIRECTIONS,
        default=DIRECTIONS[0][0],
        help_text=_('Every node must be either a revenue or expenditure node.')
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children'
    )
    inverse = models.ManyToManyField(
        'self',
        symmetrical=True,
        null=True,
        blank=True,
        related_name='inverses',
        help_text=_('Inverse relations across revenue and expenditure nodes.')
    )
    path = models.CharField(
        _('Path'),
        db_index=True,
        max_length=255,
        null=True,
        blank=True,
        editable=False,
        help_text=_('A representation of the path to the root of the template '
                    'from this template node.')
    )
    backwards = models.ManyToManyField(
        'self',
        null=True,
        blank=True,
        symmetrical=False,
        related_name='forwards'
    )

    referencesources = generic.GenericRelation(
        ReferenceSource
    )
    auxsources = generic.GenericRelation(
        AuxSource
    )

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

    def _get_path_to_root(self):
        path = [self.code]
        if self.parent:
            parent_path = self.parent._get_path_to_root()
            if parent_path:
                path = path + parent_path
        return path

    def save(self, *args, **kwargs):
        # TODO: Also need to handle path creation on updates, not only created.
        if not self.id:
            # set the `path` property if not set and needed
            if not self.path:
                self.path = PATH_SEPARATOR.join(self._get_path_to_root())

        return super(TemplateNode, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _('template node')
        verbose_name_plural = _('template nodes')

    @models.permalink
    def get_absolute_url(self):
        return 'template_node', [self.uuid]

    def __unicode__(self):
        return self.code


def inverse_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'pre_add':
        # validate that inverse never points to self
        if instance.pk in pk_set:
            raise ValidationError(_('Inverse node can not point to self.'))
        # validate that it always points to the opposite `direction`
        if model.objects.filter(pk__in=pk_set, direction=instance.direction)\
            .count():
            raise ValidationError(_("Inverse node's direction can not be the "
                                    "same as self direction."))


m2m_changed.connect(inverse_changed, sender=TemplateNode.inverse.through)


class TemplateNodeRelationManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map(self):
        return self.select_related()

    def has_same_node(self, node, template):
        return self.filter(
            node__code=node.code,
            node__name=node.name,
            node__parent=node.parent,
            template=template
        ).count()


class TemplateNodeRelation(models.Model):
    """A relation between a node and a template"""

    objects = TemplateNodeRelationManager()

    template = models.ForeignKey(
        Template
    )
    node = models.ForeignKey(
        TemplateNode
    )

    def validate_unique(self, exclude=None):
        """Custom validation for our use case."""

        super(TemplateNodeRelation, self).validate_unique(exclude)

        if not bool(self.__class__.objects.has_same_node(self.node, self.template)):
            raise ValidationError(_('Node with name: {name}; code: {code}; '
                                    'parent: {parent}; already exists in '
                                    'template: {template}'.format(
                                  name=self.node.name, code=self.node.code,
                                  parent=self.node.parent,
                                  template=self.template)))

    class Meta:
        ordering = ['template__name', 'node__name']
        verbose_name = _('template/node relation')
        verbose_name = _('template/node relations')
        unique_together = (
            ('node', 'template')
        )

    def __unicode__(self):
        return '{template} -> {node}'.format(template=self.template,
                                             node=self.node)


class SheetManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map_min(self):
        return self.select_related('entity')

    def related_map(self):
        return self.select_related().prefetch_related('items')

    def latest_of(self, entity):
        return self.filter(entity=entity).latest('period_start')


class Sheet(PeriodicModel, TimeStampedModel, UUIDModel, ClassMethodMixin):
    """An abstract class for common Budget and Actual data"""

    objects = SheetManager()

    entity = models.ForeignKey(
        Entity,
        related_name='%(class)ss'
    )
    template = models.ForeignKey(
        Template,
        related_name='%(class)ss'
    )
    description = models.TextField(
        _('Description'),
        db_index=True,
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

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.period)


class Budget(Sheet):
    """The budget sheet for the given entity/period."""

    @property
    def related_actuals(self):
        tmp = Actual.objects.filter(entity=self.entity)
        value = [actual for actual in tmp if actual.period == self.period]
        return value

    class Meta:
        ordering = ['entity']
        verbose_name = _('budget')
        verbose_name_plural = _('budgets')

    @models.permalink
    def get_absolute_url(self):
        return 'budget_detail', [self.uuid]


class Actual(Sheet):
    """The actuals sheet for the given entity/period."""

    @property
    def related_budgets(self):
        tmp = Budget.objects.filter(entity=self.entity)
        value = [budget for budget in tmp if budget.period == self.period]
        return value

    @property
    def variance(self):
        totals = None
        if self.related_budgets:
            totals = [budget.total for budget in self.related_budgets]
        total_sum = sum(totals)
        # Note: we imported division from __future__
        value = round(self.total / total_sum * 100, 2)
        return value

    class Meta:
        ordering = ['entity']
        verbose_name = _('actual')
        verbose_name_plural = _('actuals')

    @models.permalink
    def get_absolute_url(self):
        return 'actual_detail', [self.uuid]


class SheetItemManager(models.Manager):
    """Exposes the related_map method for more efficient bulk select queries."""

    def related_map_min(self):
        return self.select_related()

    def related_map(self):
        return self.select_related().prefetch_related('discussion')

    def timeline(self, node_uuid, entity_uuid):
        try:
            node = TemplateNode.objects.get(uuid=node_uuid)
        except TemplateNode.DoesNotExist as e:
            raise e
        value = self.model.objects.filter(node__in=node.timeline,
                                          budget__entity__uuid=entity_uuid)
        return value


class SheetItem(TimeStampedModel, UUIDModel, ClassMethodMixin):
    """Abstract class for common BudgetItem and ActualItem data"""

    objects = SheetItemManager()

    node = models.ForeignKey(
        TemplateNode,
        related_name='%(class)ss',
    )
    description = models.TextField(
        _('Description'),
        db_index=True,
        blank=True,
        help_text=_('Description that appears for this entry.')
    )
    amount = models.DecimalField(
        _('Amount'),
        db_index=True,
        max_digits=26,
        decimal_places=2,
        help_text=_('The total amount of this entry.')
    )
    discussion = generic.GenericRelation(
        Comment,
        object_id_field="object_pk"
    )

    referencesources = generic.GenericRelation(
        ReferenceSource
    )
    auxsources = generic.GenericRelation(
        AuxSource
    )

    @property
    def name(self):
        value = self.node.name
        return value

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.node.code


class BudgetItem(SheetItem):
    """A single item in a given budget sheet."""

    budget = models.ForeignKey(
        Budget,
        related_name='items'
    )

    class Meta:
        ordering = ['node']
        verbose_name = _('budget item')
        verbose_name_plural = _('budget items')

    @models.permalink
    def get_absolute_url(self):
        return 'budget_item_detail', [self.uuid]


class ActualItem(SheetItem):
    """A single item in a given actuals sheet."""

    actual = models.ForeignKey(
        Actual,
        related_name='items'
    )

    class Meta:
        ordering = ['node']
        verbose_name = _('actual item')
        verbose_name_plural = _('actual items')

    @models.permalink
    def get_absolute_url(self):
        return 'actual_item_detail', [self.uuid]
