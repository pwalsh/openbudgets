from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .utilities import is_comparable


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
        except self.__class__.DoesNotExist:
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
                self.path.split(self.PATH_DELIMITER)
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
