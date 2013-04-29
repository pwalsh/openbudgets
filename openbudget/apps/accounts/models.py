from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext as _
from openbudget.settings.base import LANGUAGE_CODE, LANGUAGES
from openbudget.apps.interactions.models import Star, Follow
from openbudget.commons.mixins.models import UUIDModel


class Account(UUIDModel, AbstractUser):
    """Extends Django's User with our project specific user fields"""

    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default=LANGUAGE_CODE,
        help_text=_('Set your prefered language for the app')
    )

    @property
    def comments(self):
        value = Comment.objects.filter(user=self)
        return value

    @property
    def stars(self):
        value = Star.objects.filter(user=self)
        return value

    @property
    def follows(self):
        value = Follow.objects.filter(user=self)
        return value

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    class Meta:
        ordering = ['username', 'email']
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')

    @models.permalink
    def get_absolute_url(self):
        return ('account_detail', [self.uuid])

    def __unicode__(self):
        return self.username


class UserProxyBase(Account):
    """A proxy object so we can treat different users types distinctly.

    Heavily used in the admin to customize how user accounts
    are managed from there.
    """

    class Meta:
        proxy = True

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
        profile, created = Account.objects.get_or_create(user=self)


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
        profile, created = Account.objects.get_or_create(user=self)


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
        profile, created = Account.objects.get_or_create(user=self)
