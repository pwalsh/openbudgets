from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.comments.managers import CommentManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel


class ToggleableInteractionManager(models.Manager):
    """Helpers for querying Toggleable Interaction objects"""

    def of_user(self, user):
        """Get this user's objects for this interaction"""
        return self.get_query_set().filter(user=user)


class ToggleableInteraction(TimeStampedModel, models.Model):
    """An abstract class for toggleable user interactions with objects"""

    objects = ToggleableInteractionManager()

    user = models.ForeignKey(
        User
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

    class Meta:
        abstract = True
        ordering = ['user', 'content_type', 'object_id']
        unique_together = (
            ('user', 'content_type', 'object_id'),
        )
    
    def __unicode__(self):
        return "{user} <> {obj}".format(
            user=self.user,
            obj=self.content_object
        )


class Star(ToggleableInteraction):
    """Objects that are starred by users"""

    class Meta:
        verbose_name = _('Star')
        verbose_name_plural = _('Stars')


class Follow(ToggleableInteraction):
    """Objects that are followed by users"""

    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follow')
