from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from openbudget.settings.base import AUTH_USER_MODEL
from openbudget.commons.mixins.models import TimeStampedMixin


class InteractionManager(models.Manager):
    """Helpers for querying Interaction objects"""

    def of_user(self, user):
        """Get this user's objects for this interaction"""
        return self.get_query_set().filter(user=user)


class Interaction(TimeStampedMixin):
    """An abstract class for user-object interactions"""

    objects = InteractionManager()

    user = models.ForeignKey(
        AUTH_USER_MODEL
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

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    @models.permalink
    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def __unicode__(self):
        return "{user} <> {obj}".format(
            user=self.user,
            obj=self.content_object
        )

    class Meta:
        abstract = True
        ordering = ['user', 'content_type', 'object_id']
        unique_together = (
            ('user', 'content_type', 'object_id'),
        )


class Star(Interaction):
    """Objects that are starred by users"""

    class Meta:
        verbose_name = _('Star')
        verbose_name_plural = _('Stars')


class Follow(Interaction):
    """Objects that are followed by users"""

    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')


class Share(Interaction):
    """TODO: Objects that are shared by users"""

    class Meta:
        verbose_name = _('Share')
        verbose_name_plural = _('Shares')
