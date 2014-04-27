from __future__ import division
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from openbudgets.apps.accounts.models import Account
from openbudgets.apps.entities.models import Division, Entity
from openbudgets.commons.mixins import models as mixins
from . import managers
from . import abstract_models
from .utilities import is_node_comparable


class Template(mixins.UUIDPKMixin, mixins.PeriodStartMixin,
               mixins.TimeStampMixin, mixins.ClassMethodMixin):

    """The Template model describes the structure of a Sheet.

    In Open Budgets, Sheets are the modeled representation of budget and actual
    data for Entities.

    Sheet/SheetItem objects get their structure from Template/TemplateNode
    objects.

    A Template can and usually does apply for more than one Sheet. This is the
    basis of the Open Budgets comparative analysis implementation.

    """

    class Meta:
        ordering = ['name']
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    objects = managers.TemplateManager()

    divisions = models.ManyToManyField(
        Division,
        verbose_name=_('divisions'),
        related_name='templates',)

    blueprint = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='instances',
        verbose_name=_('blueprint'),)

    name = models.CharField(
        _('Name'),
        db_index=True,
        max_length=255,
        help_text=_('The name of this template.'),)

    description = models.TextField(
        _('Description'),
        blank=True,
        help_text=_('An overview text for this template.'),)

    @property
    def node_count(self):
        return self.nodes.count()

    @property
    def has_sheets(self):
        return bool(self.sheets.count())

    @property
    def sheet_count(self):
        return self.nodes.count()

    @property
    def period(self):
        """Returns the applicable period of this template.

        If the Template instance has divisions (self.divisions.all()),
        objects are valid until the next object with a period_start in the
        future from this one, or, until 'now' if there is no future object.

        In the current case of multi-period ranges, returns a tuple of
        datetime.year objects.
        """

        start, end = None, None
        ranges = settings.OPENBUDGETS_PERIOD_RANGES

        # TODO: Support ranges other than yearly, including multiple ranges.
        if len(ranges) == 1 and 'yearly' in ranges:
            start = self.period_start.year
            if self.is_blueprint:
                objs = self.__class__.objects.filter(
                    divisions__in=self.divisions.all())
                for obj in objs:
                    if obj.period_start.year > self.period_start.year:
                        end = obj.period_start.year
                    else:
                        end = datetime.datetime.now().year
            else:
                # We have 'implementation' templates that use a blueprint
                # as a model, and implement a variant structure based on it.
                # Such templates are used by single entities, and may be
                # employed by one or many sheets for that entity.
                objs = self.sheets.all()
                years = [obj.period_start.year for obj in objs].sort()
                if not years:
                    end = start
                else:
                    end = years[-1]

        return start, end

    @property
    def is_blueprint(self):
        """Returns True if the Template is a blueprint, false otherwise.

        Blueprints are Templates that serve as structural models for other
        templates.

        Blueprints must be assigned to Divisions - they are blueprints for
        Sheets of the Entities in their Division(s).

        """

        if not self.divisions.all():
            return False
        return True

    def get_absolute_url(self):
        return reverse('template_detail', [self.id])

    def __unicode__(self):
        return self.name


class TemplateNode(abstract_models.AbstractNode, abstract_models.AbstractNodeRelations,
                   mixins.UUIDPKMixin, mixins.SelfParentMixin, mixins.TimeStampMixin,
                   mixins.ClassMethodMixin):

    """The TemplateNode model implements the structure of a Sheet.

    In Open Budgets, Sheets are the modeled representation of budget and actual
    data for Entities.

    Sheet / SheetItem objects get their structure from Template / TemplateNode
    objects.

    A TemplateNode can and usually does apply for more than one Template.
    This is the basis of the Open Budgets comparative analysis implementation.

    """

    class Meta:
        ordering = ['code', 'name']
        verbose_name = _('Template Node')
        verbose_name_plural = _('Template Nodes')

    objects = managers.TemplateNodeManager()

    templates = models.ManyToManyField(
        Template,
        through='TemplateNodeRelation',
        related_name='nodes',)

    @property
    def past(self):
        """Returns a list of past nodes that morph to this one."""

        nodes = list(self.backwards.all())

        if len(nodes):
            for node in nodes:
                nodes += node.past

        return nodes

    @property
    def future(self):
        """Returns a list of future nodes that stem from this one."""

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

    def timeline(self, include_future=False):
        """Returns this node's full timeline as a list."""

        timeline = self.with_past

        if include_future:
            timeline += self.future

        return timeline

    def get_absolute_url(self):
        return reverse('template_node', [self.id])

    def __unicode__(self):
        return self.code

    def clean(self):

        if self.parent and not self.direction == self.parent.direction:
            raise ValidationError('A node must have the same direction as its '
                                  'parent.')

        if self.parent is self:
            raise ValidationError('A node cannot be its own parent.')


def inverse_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Validating m2m relations on TemplateNode."""

    if action == 'pre_add':

        # validate that inverse never points to self
        if instance.pk in pk_set:
            raise ValidationError(_('Inverse node can not point to self.'))

        # validate that it always points to the opposite `direction`
        if model.objects.filter(pk__in=pk_set,
                                direction=instance.direction).count():
            raise ValidationError(_("Inverse node's direction can not be the "
                                    "same as self direction."))


m2m_changed.connect(inverse_changed, sender=TemplateNode.inverse.through)


class TemplateNodeRelation(models.Model):

    """A custom through table for relations between nodes and templates."""

    class Meta:
        ordering = ['template__name', 'node__name']
        verbose_name = _('Template/TemplateNode Relation')
        verbose_name = _('Template/TemplateNode Relations')
        unique_together = (('node', 'template'),)

    objects = managers.TemplateNodeRelationManager()

    template = models.ForeignKey(
        Template,)

    node = models.ForeignKey(
        TemplateNode,)

    def __unicode__(self):
        return '{template} -> {node}'.format(template=self.template,
                                             node=self.node)

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

    def save(self, *args, **kwargs):
        super(TemplateNodeRelation, self).save(*args, **kwargs)

        # have to do this here because our logic needs to know the template(s)
        # of the node
        self.node.comparable = is_node_comparable(self.node)
        self.node.save()


class Sheet(mixins.UUIDPKMixin, mixins.PeriodicMixin, mixins.TimeStampMixin,
            mixins.ClassMethodMixin):

    """The Sheet model describes the declared budgetary data of a given period,
     for a given entity.

    In Open Budgets, Sheet / SheetItem objects get their structure from
    Template / TemplateNode objects.

    A Template can and usually does apply for more than one Sheet. This is the
    basis of the Open Budgets comparative analysis implementation.

    """

    objects = managers.SheetManager()

    class Meta:
        ordering = ('entity', 'period_start')
        get_latest_by = 'period_start'
        verbose_name = _('Sheet')
        verbose_name_plural = _('Sheets')

    entity = models.ForeignKey(
        Entity,
        related_name='sheets',
        help_text=_('The entity this sheet belongs to.'),)

    template = models.ForeignKey(
        Template,
        related_name='sheets',
        help_text=_('The template used to structure this sheet.'),)

    budget = models.DecimalField(
        _('budget'),
        db_index=True,
        max_digits=26,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The total budget amount for this sheet.'),)

    actual = models.DecimalField(
        _('actual'),
        db_index=True,
        max_digits=26,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The total actual amount for this sheet.'),)

    description = models.TextField(
        _('description'),
        db_index=True,
        blank=True,
        help_text=_('An introductory description for this sheet.'),)

    @property
    def item_count(self):
        value = self.items.all().count()
        return value

    @property
    def variance(self):
        """Returns variance between budget and actual as a percentage."""

        if not self.actual or not self.budget:
            return None
        # Note: we imported division from __future__ for py3 style division
        value = round(self.actual / self.budget * 100, 2)
        return value

    def get_absolute_url(self):
        return reverse('sheet_detail', [self.id])

    def __unicode__(self):
        return unicode(self.period)


class SheetItem(abstract_models.AbstractItem, abstract_models.AbstractNode,
                mixins.UUIDPKMixin, mixins.SelfParentMixin, mixins.TimeStampMixin,
                mixins.ClassMethodMixin):

    """The SheetItem model describes items of budgetary data of a given period,
     for a given entity.

    In Open Budgets, Sheet / SheetItem objects get their structure from
    Template / TemplateNode objects.

    A Template can and usually does apply for more than one Sheet. This is the
    basis of the Open Budgets comparative analysis implementation.

    """

    DIRECTIONS = (('REVENUE', _('Revenue')), ('EXPENDITURE', _('Expenditure')),)

    PATH_DELIMITER = settings.OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER

    class Meta:
        ordering = ['node']
        verbose_name = _('sheet item')
        verbose_name_plural = _('sheet items')
        unique_together = (('sheet', 'node'),)

    objects = managers.SheetItemManager()

    sheet = models.ForeignKey(
        Sheet,
        related_name='items',)

    node = models.ForeignKey(
        TemplateNode,
        related_name='items',)

    has_comments = models.BooleanField(
        _('Has Comments?'),
        default=False)

    comment_count = models.PositiveSmallIntegerField(
        _('Comment Count'),
        default=0)

    def get_absolute_url(self):
        return reverse('sheet_item_detail', [self.pk])

    def __unicode__(self):
        return self.node.code

    def save(self, *args, **kwargs):

        # set the fields that we denormalized from the node
        for field in abstract_models.AbstractNode._meta.get_all_field_names():
            setattr(self, field, getattr(self.node, field))

        # set the comment data fields to something other than default, maybe
        if (self.description or self.comment_count > 0):
            self.has_comments = True

        if self.description and self.comment_count == 0:
            self.comment_count = 1

        super(SheetItem, self).save(*args, **kwargs)


class SheetItemComment(mixins.UUIDPKMixin, mixins.TimeStampMixin,
                       mixins.ClassMethodMixin):

    """Records discussion around particular budget items."""

    class Meta:
        ordering = ['user', 'last_modified']
        verbose_name = _('sheet item comment')
        verbose_name_plural = _('sheet item comments')

    objects = managers.SheetItemCommentManager()

    item = models.ForeignKey(
        SheetItem,
        related_name='discussion',)

    user = models.ForeignKey(
        Account,
        related_name='item_comments',)

    comment = models.TextField(
        _('Comment'),
        help_text=_('Add your comments to this discussion.'),)

    def __unicode__(self):
        return self.comment


@receiver(post_save, sender=SheetItemComment)
def update_item_comment_count(sender, instance, created, **kwargs):
    if created:
        instance.item.comment_count += 1
        instance.item.save()
    return instance
