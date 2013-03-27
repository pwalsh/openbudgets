from django.db import models
from django.db.models.loading import get_model
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from taggit.models import ItemBase as TaggitItemBase
from autoslug import AutoSlugField
from slugify import slugify as unislugify
from openbudget.apps.budgets.models import BudgetTemplateNode
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel
from openbudget.commons.data import OBJECT_STATES


# Our models need to impement tags like so:
# labels = TaggableManager(through=LabeledItem)


class Taxonomy(TimeStampedModel, UUIDModel, models.Model):

    user = models.ForeignKey(
        User,
        related_name='taxonomies'
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('The name of this taxonomy.')
    )

    description = models.TextField(
        _('Taxonomy description'),
        blank=True,
        help_text=_('Describe the purpose and goals of this taxonomy.')
    )

    status = models.IntegerField(
        _('Publication status'),
        choices=OBJECT_STATES,
        default=1,
        help_text=_('Determines whether the taxonomy is publically viewable.')
    )

    slug = AutoSlugField(
        populate_from='name',
        unique=True
    )

    @property
    def count(self):
        value = self.tags.count()
        return value

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('taxonomy_detail', [self.slug])

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    class Meta:
        verbose_name = _("Taxonomy")
        verbose_name_plural = _("Taxonomies")
        unique_together = (
            ('user', 'name'),
        )


class TagManager(models.Manager):

    def get_queryset(self):
        taxonomy = Taxonomy.objects.get(
            slug=self.kwargs['taxonomy_slug']
        )
        return super(TagManager, self).get_queryset().filter(
            taxonomy=taxonomy
        )

class Tag(models.Model):
    """A tag with full unicode support."""

    taxonomy = models.ForeignKey(
        Taxonomy,
        related_name='tags'
    )

    name = models.CharField(
        _('Name'),
        max_length=100
    )

    slug = AutoSlugField(
        populate_from='name',
        unique=True
    )

    @models.permalink
    def get_absolute_url(self):
        return ('tag_detail', [self.taxonomy.slug, self.slug])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        unique_together = (
            ('name', 'taxonomy'),
        )


class TaggedNode(TaggitItemBase):

    tag = models.ForeignKey(
        Tag,
        related_name='tags'
    )

    content_object = models.ForeignKey(
        BudgetTemplateNode,
        related_name='tags'
    )

    @classmethod
    def tags_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "%s__content_type" % cls.tag_relname(): ct
        }
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk
        return cls.tag_model().objects.filter(**kwargs).distinct()

    class Meta:
        verbose_name = _("Tagged node")
        verbose_name_plural = _("Tagged nodes")
