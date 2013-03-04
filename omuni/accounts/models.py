from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from omuni.settings.base import LANGUAGES
from omuni.interactions.models import IComment, Post, Annotation, Star, Follow
from omuni.commons.mixins.models import UUIDModel


class UserProfile(UUIDModel, models.Model):
    """Extends Django's User with our project specific user fields"""

    user = models.OneToOneField(
        User
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default='en',
        help_text=_('Set your prefered language for the app')
    )

    @property
    def posts(self):
        # We'll use proxy models to get the actual discussions
        value = Post.objects.filter(user=self.user)
        return value

    @property
    def annotations(self):
        # We'll use proxy models to get the actual annotations
        value = Annotation.objects.filter(user=self.user)
        return value

    @property
    def stars(self):
        value = Star.objects.filter(user=self.user)
        return value

    @property
    def follows(self):
        value = Follow.objects.filter(user=self.user)
        return value

    class Meta:
        ordering = ['user']
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')

    @models.permalink
    def get_absolute_url(self):
        return ('user_profile_detail', [self.uuid])

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    """A new UserProfile is created for every new User created."""
    if created:
        UserProfile.objects.create(user=instance)


class UserProxyBase(User):
    """A proxy object so we can treat different users types distinctly.

    Heavily used in the admin to customize how user accounts
    are managed from there.
    """

    class Meta:
        proxy = True

    @property
    def uuid(self):
        tmp = UserProfile.objects.get(user=self)
        value = tmp.uuid
        return value

    @property
    def language(self):
        tmp = UserProfile.objects.get(user=self)
        value = tmp.language
        return value

    def __unicode__(self):
        return self.username


class CoreTeamUserProxyManager(models.Manager):
    """Filter core team user proxy queries correctly"""

    def get_query_set(self):
        return super(CoreTeamUserProxyManager, self).get_query_set().filter(groups__in=[1])


class CoreTeamUserProxy(UserProxyBase):
    """Provides a proxy interface to users on the core team"""

    objects = CoreTeamUserProxyManager()

    class Meta:
        proxy = True
        verbose_name = _('Core team user')
        verbose_name_plural = _('Core team users')

    def save(self, *args, **kwargs):
        super(CoreTeamUserProxy, self).save(*args, **kwargs)
        self.groups.add(1)
        profile, created = UserProfile.objects.get_or_create(user=self)


class ContentTeamUserManager(models.Manager):
    """Filter content team user proxy queries correctly"""

    def get_query_set(self):
        return super(ContentTeamUserManager, self).get_query_set().filter(groups__in=[2])


class ContentTeamUserProxy(UserProxyBase):
    """Provides a proxy interface to users on the content team"""

    objects = ContentTeamUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Content team user')
        verbose_name_plural = _('Content team users')

    def save(self, *args, **kwargs):
        super(ContentTeamUserProxy, self).save(*args, **kwargs)
        self.groups.add(2)
        profile, created = UserProfile.objects.get_or_create(user=self)


class PublicUserProxyManager(models.Manager):
    """Filter public user proxy queries correctly"""

    def get_query_set(self):
        return super(PublicUserProxyManager, self).get_query_set().filter(groups__in=[3])


class PublicUserProxy(UserProxyBase):
    """Provides a proxy interface to public users"""

    objects = PublicUserProxyManager()

    class Meta:
        proxy = True
        verbose_name = _('Public user')
        verbose_name_plural = _('Public users')

    def save(self, *args, **kwargs):
        super(PublicUserProxy, self).save(*args, **kwargs)
        self.groups.add(3)
        profile, created = UserProfile.objects.get_or_create(user=self)
