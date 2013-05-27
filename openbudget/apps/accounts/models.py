from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext as _
from openbudget.settings import base as settings
from openbudget.apps.interactions.models import Star, Follow
from openbudget.commons.mixins.models import UUIDModel


class Account(UUIDModel, AbstractUser):
    """Extends Django's User with our project specific user fields"""

    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        help_text=_('Set your preferred language for the app')
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


class AccountProxyBase(Account):
    """A proxy object so we can treat different users types distinctly.

    Heavily used in the admin to customize how user accounts
    are managed from there.
    """

    class Meta:
        proxy = True

    def __unicode__(self):
        return self.username


class CoreTeamAccountManager(models.Manager):
    """Filter core team user proxy queries correctly"""

    def get_query_set(self):
        return super(CoreTeamAccountManager, self).get_query_set().filter(
            groups=settings.OPENBUDGET_CORE_TEAM_ID)


class CoreTeamAccount(AccountProxyBase):
    """Provides a proxy interface to users on the core team"""

    objects = CoreTeamAccountManager()

    class Meta:
        proxy = True
        verbose_name = _('Core team user')
        verbose_name_plural = _('Core team users')

    def save(self, *args, **kwargs):
        super(CoreTeamAccount, self).save(*args, **kwargs)
        self.groups.add(settings.OPENBUDGET_CORE_TEAM_ID)


class ContentTeamAccountManager(models.Manager):
    """Filter content team user proxy queries correctly"""

    def get_query_set(self):
        return super(ContentTeamAccountManager, self).get_query_set().filter(
            groups=settings.OPENBUDGET_CONTENT_TEAM_ID)


class ContentTeamAccount(AccountProxyBase):
    """Provides a proxy interface to users on the content team"""

    objects = ContentTeamAccountManager()

    class Meta:
        proxy = True
        verbose_name = _('Content team user')
        verbose_name_plural = _('Content team users')

    def save(self, *args, **kwargs):
        super(ContentTeamAccount, self).save(*args, **kwargs)
        self.groups.add(settings.OPENBUDGET_CONTENT_TEAM_ID)


class PublicAccountManager(models.Manager):
    """Filter public user proxy queries correctly"""

    def get_query_set(self):
        return super(PublicAccountManager, self).get_query_set().filter(
            groups=settings.OPENBUDGET_PUBLIC_ID)


class PublicAccount(AccountProxyBase):
    """Provides a proxy interface to public users"""

    objects = PublicAccountManager()

    class Meta:
        proxy = True
        verbose_name = _('Public user')
        verbose_name_plural = _('Public users')

    def save(self, *args, **kwargs):
        super(PublicAccount, self).save(*args, **kwargs)
        self.groups.add(settings.OPENBUDGET_PUBLIC_ID)
