from __future__ import division
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed
from django.utils.translation import ugettext_lazy as _
from openbudgets.apps.accounts.models import Account
from openbudgets.apps.entities.models import Division, Entity
from openbudgets.commons.mixins import models as mixins
from . import managers
from . import abstract_models


class Template(mixins.UUIDPKMixin, mixins.PeriodStartMixin,
               mixins.TimeStampedMixin, mixins.ClassMethodMixin):

    """The Template model describes the structure of a Sheet.

    In Open Budgets, Sheets are the modeled representation of budget and actual
    data for Entities.

    Sheets / SheetItems get their structure from Templates / TemplateNodes.

    A Template can and usually does apply for more than one Sheet. This is the
    basis of the Open Budgets comparative analysis implementation.

    """

    class Meta:
        ordering = ['name']
        verbose_name = _('template')
        verbose_name_plural = _('templates')

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

    @property
    def has_sheets(self):
        return bool(self.sheets.count())

    def get_absolute_url(self):
        return reverse('template_detail', [self.id])

    def __unicode__(self):
        return self.name


class TemplateNode(abstract_models.AbstractBaseNode, mixins.UUIDPKMixin,
                   mixins.TimeStampedMixin):

    """The TemplateNode model implements the structure of a Sheet.

    In Open Budgets, Sheets are the modeled representation of budget and actual
    data for Entities.

    Sheets / SheetItems get their structure from Templates / TemplateNodes.

    A TemplateNode can and usually does apply for more than one Template.
    This is the basis of the Open Budgets comparative analysis implementation.

    """

    class Meta:
        ordering = ['code', 'name']
        verbose_name = _('template node')
        verbose_name_plural = _('template nodes')

    objects = managers.TemplateNodeManager()

    templates = models.ManyToManyField(
        Template,
        through='TemplateNodeRelation',
        related_name='nodes',)

    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('A descriptive text for this template node.'),)

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
        verbose_name = _('template/node relation')
        verbose_name = _('template/node relations')
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

        if not bool(self.__class__.objects.has_same_node(
                self.node, self.template)):
            raise ValidationError(_('Node with name: {name}; code: {code}; '
                                    'parent: {parent}; already exists in '
                                    'template: {template}'.format(
                                  name=self.node.name, code=self.node.code,
                                  parent=self.node.parent,
                                  template=self.template)))


class Sheet(mixins.UUIDPKMixin, mixins.PeriodicMixin, mixins.TimeStampedMixin,
            mixins.ClassMethodMixin):

    """The Sheet model describes the declared budgetary data of a given period,
     for a given entity.

    In Open Budgets, Sheets / SheetItems get their structure from
    Templates / TemplateNodes.

    A Template can and usually does apply for more than one Sheet. This is the
    basis of the Open Budgets comparative analysis implementation.

    """

    objects = managers.SheetManager()

    class Meta:
        ordering = ('entity', 'period_start')
        get_latest_by = 'period_start'
        verbose_name = _('sheet')
        verbose_name_plural = _('sheets')

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


class SheetItem(abstract_models.AbstractBaseItem, mixins.UUIDPKMixin,
                mixins.TimeStampedMixin, mixins.ClassMethodMixin):

    """The SheetItem model describes items of budgetary data of a given period,
     for a given entity.

    In Open Budgets, Sheets / SheetItems get their structure from
    Templates / TemplateNodes.

    A Template can and usually does apply for more than one Sheet. This is the
    basis of the Open Budgets comparative analysis implementation.

    """

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

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        editable=False,
        related_name='children',)

    @property
    def lookup(self):
        return self.node.pk

    @property
    def name(self):
        return self.node.name

    @property
    def code(self):
        return self.node.code

    @property
    def comparable(self):
        return self.node.comparable

    @property
    def direction(self):
        return self.node.direction

    @property
    def path(self):
        return self.node.path

    @property
    def depth(self):
        return self.node.depth

    @property
    def has_comments(self):
        return len(self.description) or self.discussion.exists()

    @property
    def comment_count(self):
        count = 0
        if self.description:
            count = 1
        count += self.discussion.count()
        return count

    @property
    def ancestors(self):
        ancestors = []
        current = self
        try:
            while current:
                parent = current.parent
                if parent:
                    ancestors.append(parent)
                current = parent
        except TemplateNode.DoesNotExist:
            pass
        ancestors.reverse()
        return ancestors

    def get_absolute_url(self):
        return reverse('sheet_item_detail', [self.pk])

    def __unicode__(self):
        return self.node.code


class SheetItemComment(mixins.UUIDPKMixin, mixins.TimeStampedMixin,
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
