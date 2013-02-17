from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from omuni.commons.mixins.models import TimeStampedModel, UUIDModel


class Remark(TimeStampedModel, UUIDModel, Comment):
    """Just a comment, really"""
    #title = models.CharField(max_length=300)
    pass


class RemarkProxyBase(Remark):

    class Meta:
        proxy = True


class Opinion(RemarkProxyBase):

    class Meta:
        proxy = True
        verbose_name = _('Opinion')
        verbose_name_plural = _('Opinions')


class Annotation(RemarkProxyBase):

    class Meta:
        proxy = True
        verbose_name = _('Annotation')
        verbose_name_plural = _('Annotations')


class ToggleableInteractionManager(models.Manager):
    """Helpers for querying Toggleable Interaction objects"""

    def of_user(self, user):
        """Get this user's objects for this interaction"""
        return self.get_query_set().filter(user=user)

    @classmethod
    def toggle(cls, content_object, user):
        """Toggle interaction state for this object/user combo.

        Example: If the given object is already starred for
        this user, then toggle unstars, and vice versa.
        """
        content_type = ContentType.objects.get_for_model(
            type(content_object)
        )

        try:
            # if it exists, then we are deleting it
            interaction = self.of_user.get(
                content_type=content_type,
                object_id=content_object.pk,
                content_object=content_object
            )
            interaction.delete()

        except Star.DoesNotExist:
            # if it doesn't exist, we are creating it
            interaction = self.model.objects.create(
                user=user,
                content_type=content_type,
                object_id=content_object.pk,
                content_object=content_object
            )
            interaction.save()

        return interaction


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
