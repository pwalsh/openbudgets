from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from openbudgets.commons.mixins import models as mixins


class InteractionManager(models.Manager):

    """Helpers for querying Interaction objects"""

    def of_user(self, user):
        """Get this user's objects for this interaction"""
        return self.get_query_set().filter(user=user)


class Interaction(mixins.TimeStampMixin, mixins.ClassMethodMixin):

    """An abstract class for user-object interactions"""

    class Meta:
        abstract = True
        ordering = ['user', 'content_type', 'object_id']
        unique_together = (('user', 'content_type', 'object_id'),)

    objects = InteractionManager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,)

    content_type = models.ForeignKey(
        ContentType,
        editable=False,)

    object_id = models.PositiveIntegerField(
        editable=False,)

    content_object = generic.GenericForeignKey(
        'content_type', 'object_id',)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def __unicode__(self):
        return "{user} <> {obj}".format(user=self.user, obj=self.content_object)


class Star(Interaction):

    """Objects that are starred by users"""

    class Meta:
        verbose_name = _('star')
        verbose_name_plural = _('stars')


class Follow(Interaction):

    """Objects that are followed by users"""

    class Meta:
        verbose_name = _('follow')
        verbose_name_plural = _('follows')


class Share(Interaction):

    """TODO: Objects that are shared by users"""

    class Meta:
        verbose_name = _('share')
        verbose_name_plural = _('shares')
