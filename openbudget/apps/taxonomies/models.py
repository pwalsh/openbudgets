from django.db import models
from django.db.models.loading import get_model
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from taggit.models import GenericTaggedItemBase, TagBase
from autoslug import AutoSlugField
from slugify import slugify as unislugify
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel


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


class TaxonomyTag(TagBase):
    """Supporting proper unicode slugs.

    Attention:

    Django's SlugField is a curse when you want
    unicode slugs. In most places in the code base, we can
    elegantly deal with it using AutoSlugField and mozilla's
    unicode-friendly slugify function. Using 3rd party apps
    is a *bit* more problematic. I considered forking taggit
    to directly replace the SlugField with with the above
    solution. I compromised and instead implemented here a
    unislug field.

    Note that I *still* unislugify the inherited slug field, but
    this will break if you try to use it directly with Django's
    url resolver from templates: {% url 'tag_view' tag.slug %}

    In this solution, the compromise requires:
    {% url 'tag_view' tag.unislug %}

    """

    taxonomy = models.ForeignKey(
        Taxonomy,
        related_name='tags'
    )

    unislug = AutoSlugField(
        populate_from='name',
        unique=True
    )

    def slugify(self, tag, i=None):
        slug = unislugify(self.name)
        if i is not None:
            slug += "_%d" % i
        return slug

    class Meta:
        verbose_name = _("Taxonomy tag")
        verbose_name_plural = _("Taxonomy tags")


class TaxonomyTaggedItem(GenericTaggedItemBase):

    tag = models.ForeignKey(
        TaxonomyTag,
        related_name="tags"
    )

    class Meta:
        verbose_name = _("Taxonomy tagged item")
        verbose_name_plural = _("Taxonomy tagged items")

