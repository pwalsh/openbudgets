from __future__ import division
import datetime
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# from django.contrib.contenttypes import generic
from django.db.models.signals import m2m_changed
from openbudgets.apps.accounts.models import Account
from openbudgets.apps.entities.models import Division, Entity
# from openbudgets.apps.sources.models import ReferenceSource, AuxSource
from openbudgets.commons.mixins.models import TimeStampedMixin, UUIDPKMixin, \
    PeriodStartMixin, PeriodicMixin, ClassMethodMixin
from openbudgets.apps.sheets.utilities import is_comparable


class TemplateManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map_min(self):
        return self.select_related().prefetch_related('divisions', 'sheets')

    def related_map(self):
        return self.select_related().prefetch_related('divisions', 'sheets', 'nodes')

    #TODO: Consider better ways to do this.
    def latest_of(self, entity):
        return self.filter(sheets__entity=entity).latest('period_start')


class Template(UUIDPKMixin, PeriodStartMixin, TimeStampedMixin, ClassMethodMixin):

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

    objects = TemplateManager()

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
        db_index=True,
        blank=True,
        help_text=_('An overview text for this template.'),)

    # referencesources = generic.GenericRelation(
    #     ReferenceSource,)

    # auxsources = generic.GenericRelation(
    #     AuxSource,)

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

    @models.permalink
    def get_absolute_url(self):
        return 'template_detail', [self.id]

    def __unicode__(self):
        return self.name


class AbstractBaseNode(models.Model):

    class Meta:
        abstract = True

    DIRECTIONS = (('REVENUE', _('Revenue')), ('EXPENDITURE', _('Expenditure')),)

    PATH_DELIMITER = settings.OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER

    name = models.CharField(
        _('Name'),
        db_index=True,
        max_length=255,
        help_text=_('The name of this template node.'),)

    code = models.CharField(
        _('Code'),
        db_index=True,
        max_length=255,
        help_text=_('An identifying code for this template node.'),)

    comparable = models.BooleanField(
        _('Comparable'),
        default=is_comparable,
        help_text=_('A flag to designate whether this node is suitable for '
                    'comparison or not.'),)

    direction = models.CharField(
        _('REVENUE/EXPENDITURE'),
        db_index=True,
        max_length=15,
        choices=DIRECTIONS,
        default=DIRECTIONS[0][0],
        help_text=_('Template nodes are one of revenue or expenditure.'),)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',)

    inverse = models.ManyToManyField(
        'self',
        symmetrical=True,
        null=True,
        blank=True,
        related_name='inverses',
        help_text=_('Inverse relations across revenue and expenditure nodes.'),)

    path = models.CharField(
        _('Path'),
        db_index=True,
        max_length=255,
        editable=False,
        help_text=_('A representation of the path to the root of the template '
                    'from this template node, using codes.'),)

    backwards = models.ManyToManyField(
        'self',
        null=True,
        blank=True,
        symmetrical=False,
        related_name='forwards',)

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

    @property
    def depth(self):
        branch = self.path.split(',')
        return len(branch) - 1

    def _get_path_to_root(self):

        """Recursively build a *code* hierarchy from self to top of tree."""

        path = [self.code]

        if self.parent:
            parent_path = self.parent._get_path_to_root()

            if parent_path:
                path = path + parent_path

        return path

    def clean(self):

        if self.path and self.pk is None:
            try:
                tmp = self.path.split(self.PATH_DELIMITER)

            except ValueError:
                raise ValidationError('The delimiter symbol for path appears '
                                      'to be invalid.')

    def save(self, *args, **kwargs):

        if self.path and self.pk is None:
            # The instance creation was passed an explicit path
            # Convert it to a list with the delimiter, then, to a
            # comma-separated string.
            tmp = self.path.split(self.PATH_DELIMITER)
            self.path = ','.join(tmp)

        else:
            # Create the path recursively over parents
            self.path = ','.join(self._get_path_to_root())

        return super(AbstractBaseNode, self).save(*args, **kwargs)


class TemplateNodeManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map_min(self):
        return self.select_related('parent')

    def related_map(self):
        return self.select_related('parent').prefetch_related(
                                                              'templates',
                                                              'inverse',
                                                              'backwards',
                                                              'items')


class TemplateNode(UUIDPKMixin, AbstractBaseNode, TimeStampedMixin):

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

    objects = TemplateNodeManager()

    templates = models.ManyToManyField(
        Template,
        through='TemplateNodeRelation',
        related_name='nodes',)

    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('A descriptive text for this template node.'),)

    # referencesources = generic.GenericRelation(
    #     ReferenceSource,)

    # auxsources = generic.GenericRelation(
    #     AuxSource,)

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

    @models.permalink
    def get_absolute_url(self):
        return 'template_node', [self.id]

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


class TemplateNodeRelationManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map(self):
        return self.select_related()

    # TODO: check where is used, and implement differently.
    def has_same_node(self, node, template):
        return self.filter(node__code=node.code, node__name=node.name,
                           node__parent=node.parent, template=template).count()


class TemplateNodeRelation(models.Model):

    """A custom through table for relations between nodes and templates."""

    class Meta:
        ordering = ['template__name', 'node__name']
        verbose_name = _('template/node relation')
        verbose_name = _('template/node relations')
        unique_together = (('node', 'template'),)

    objects = TemplateNodeRelationManager()

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


class SheetManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def related_map_min(self):
        return self.select_related('entity')

    def related_map(self):
        return self.select_related().prefetch_related('items')

    # TODO: Check if we can replace this expensive query
    def latest_of(self, entity):
        return self.filter(entity=entity).latest('period_start')


class Sheet(UUIDPKMixin, PeriodicMixin, TimeStampedMixin, ClassMethodMixin):

    """The Sheet model describes the declared budgetary data of a given period,
     for a given entity.

    In Open Budgets, Sheets / SheetItems get their structure from
    Templates / TemplateNodes.

    A Template can and usually does apply for more than one Sheet. This is the
    basis of the Open Budgets comparative analysis implementation.

    """

    objects = SheetManager()

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

    # referencesources = generic.GenericRelation(
    #     ReferenceSource,)

    # auxsources = generic.GenericRelation(
    #     AuxSource,)

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

    @models.permalink
    def get_absolute_url(self):
        return 'sheet_detail', [self.id]

    def __unicode__(self):
        return unicode(self.period)


class AbstractBaseItem(models.Model):

    class Meta:
        abstract = True

    budget = models.DecimalField(
        _('budget'),
        db_index=True,
        max_digits=26,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The total budget amount for this item.'),)

    actual = models.DecimalField(
        _('actual'),
        db_index=True,
        max_digits=26,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The total actual amount for this item.'),)

    description = models.TextField(
        _('description'),
        db_index=True,
        blank=True,
        help_text=_('An introductory description for this sheet item.'),)

    @property
    def variance(self):

        """Returns variance between budget and actual as a percentage."""

        if not self.actual or not self.budget:
            return None
        # Note: we imported division from __future__ for py3 style division
        value = round(self.actual / self.budget * 100, 2)
        return value

    @property
    def period(self):
        return self.sheet.period


class SheetItemManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def get_queryset(self):
        return super(SheetItemManager, self).select_related('node')

    def related_map_min(self):
        return self.select_related()

    def related_map(self):
        return self.select_related().prefetch_related('parent__parent', 'children', 'discussion')

    # TODO: Check this for a more efficient implementation
    def timeline(self, node_pks, entity_pk):
        nodes = TemplateNode.objects.filter(id__in=node_pks)
        timelines = []
        if nodes.count():
            for node in nodes:
                timelines += node.timeline()
        else:
            raise TemplateNode.DoesNotExist()

        return self.filter(node__in=timelines, sheet__entity=entity_pk).select_related('sheet')


class SheetItem(UUIDPKMixin, AbstractBaseItem, TimeStampedMixin, ClassMethodMixin):

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

    objects = SheetItemManager()

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

    # referencesources = generic.GenericRelation(
    #     ReferenceSource,)

    # auxsources = generic.GenericRelation(
    #     AuxSource,)

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

    @models.permalink
    def get_absolute_url(self):
        return 'sheet_item_detail', [self.pk]

    def __unicode__(self):
        return self.node.code

    def save(self, *args, **kwargs):

        # SheetItem.parent is a proxy for TemplateNode.parent
        # (where we'd have to make more complex queries to get the item's parent)
        if self.node.parent and self.node.parent.items.filter(sheet=self.sheet).exists():
            tmp = self.node.path.split(',')[1:]
            parent_path = ','.join(tmp)
            candidates = self.node.parent.items.filter(sheet=self.sheet)
            self.parent = candidates.get(node__path=parent_path)

        return super(SheetItem, self).save(*args, **kwargs)


class SheetItemCommentManager(models.Manager):

    """Exposes additional methods for model query operations.

    Open Budgets makes extensive use of related_map and related_map_min methods
    for efficient bulk select queries.

    """

    def get_queryset(self):
        return super(SheetItemCommentManager, self).select_related()

    def related_map_min(self):
        return self.select_related('user')

    def related_map(self):
        return self.select_related()

    def by_item(self, item_pk):
        return self.filter(item=item_pk).related_map_min()


class SheetItemComment(UUIDPKMixin, TimeStampedMixin, ClassMethodMixin):

    """The SheetItemComment model records discussion around particular budget
    items.

    """

    class Meta:
        ordering = ['user', 'last_modified']
        verbose_name = _('sheet item comment')
        verbose_name_plural = _('sheet item comments')

    objects = SheetItemCommentManager()

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
