from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from openbudget.commons.mixins.models import TimeStampedModel, UUIDModel


COMMENT_TYPE_CHOICES = (
    ('post', _('Post')),
    ('annotation', _('Annotation')),
)


class IComment(TimeStampedModel, UUIDModel, Comment):
    """Django's Comment class with additional functionality"""

    #title = models.CharField(max_length=300)
    of_type = models.CharField(
        _('Of type'),
        max_length=20,
        choices=COMMENT_TYPE_CHOICES,
        editable=False
    )

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    def get_absolute_url(self, anchor_pattern="#comment-%(uuid)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)


class CommentProxyBase(IComment):

    class Meta:
        proxy = True


class PostManager(models.Manager):
    """Returns just Posts"""

    def get_query_set(self):
        return super(PostManager, self).get_query_set().filter(of_type='post')


class Post(CommentProxyBase):

    objects = PostManager()

    class Meta:
        proxy = True
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class AnnotationManager(models.Manager):
    """Returns just Annotations"""

    def get_query_set(self):
        return super(AnnotationManager, self).get_query_set().filter(of_type='annotation')


class Annotation(CommentProxyBase):

    objects = AnnotationManager()

    class Meta:
        proxy = True
        verbose_name = _('Annotation')
        verbose_name_plural = _('Annotations')


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
