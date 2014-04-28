from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from taggit.models import ItemBase as TaggitItemBase
from autoslug import AutoSlugField
from openbudgets.apps.sheets.models import Template, TemplateNode
from openbudgets.commons.mixins import models as mixins


# Our models need to implement tags like so:
# labels = TaggableManager(through=TaggedNode)


class Taxonomy(mixins.TimeStampMixin, mixins.UUIDMixin,
               mixins.ClassMethodMixin):

    STATUS_CHOICES = ((1, 'draft'), (2, 'published'))

    class Meta:
        verbose_name = _("Taxonomy")
        verbose_name_plural = _("Taxonomies")
        unique_together = (('user', 'name', 'template'),)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='taxonomies',)

    template = models.ForeignKey(
        Template,
        related_name='taxonomies',)

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('The name of this taxonomy.'),)

    description = models.TextField(
        _('Taxonomy description'),
        blank=True,
        help_text=_('Describe the purpose and goals of this taxonomy.'),)

    status = models.IntegerField(
        _('Publication status'),
        choices=STATUS_CHOICES,
        default=1,
        help_text=_('Determines whether the taxonomy is publically viewable.'),)

    slug = AutoSlugField(
        populate_from='name',
        unique=True,)

    @property
    def count(self):
        value = self.tags.count()
        return value

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('taxonomy_detail', [self.slug])


class TagManager(models.Manager):

    def get_queryset(self):
        taxonomy = Taxonomy.objects.get(
            slug=self.kwargs['taxonomy_slug'],)

        return super(TagManager, self).get_queryset().filter(
            taxonomy=taxonomy,
            slug=self.kwargs['taxonomy_slug'],)


class Tag(models.Model):

    """A tag with full unicode support."""

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        unique_together = (('name', 'taxonomy'),)

    taxonomy = models.ForeignKey(
        Taxonomy,
        related_name='tags',)

    name = models.CharField(
        _('Name'),
        max_length=100,)

    slug = AutoSlugField(
        populate_from='name',
        unique=False,)

    def get_absolute_url(self):
        return reverse('tag_detail', [self.taxonomy.slug, self.slug])

    def __unicode__(self):
        return self.name


class TaggedNode(TaggitItemBase, mixins.ClassMethodMixin):

    class Meta:
        verbose_name = _("Tagged node")
        verbose_name_plural = _("Tagged nodes")
        unique_together = (('tag', 'content_object'),)

    tag = models.ForeignKey(
        Tag,
        related_name='nodetags',)

    content_object = models.ForeignKey(
        TemplateNode,
        related_name='nodetags',)

    @classmethod
    def tags_for(cls, model, instance=None):
        ct = generic.ContentType.objects.get_for_model(model)
        kwargs = {"%s__content_type" % cls.tag_relname(): ct}
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk
        return cls.tag_model().objects.filter(**kwargs).distinct()
