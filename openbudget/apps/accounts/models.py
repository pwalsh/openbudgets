from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext as _
from django.utils import timezone
from openbudget.settings import base as settings
from openbudget.apps.interactions.models import Star, Follow
from openbudget.commons.mixins.models import UUIDModel, TimeStampedModel
from django_gravatar.helpers import get_gravatar_url


class AccountManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = AccountManager.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, is_staff=False, is_active=True,
                          is_superuser=False, last_login=now, created_on=now,
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        u = self.create_user(email, first_name, last_name, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class Account(UUIDModel, TimeStampedModel, PermissionsMixin, AbstractBaseUser):
    """Extends Django's User with our project specific user fields"""

    objects = AccountManager()

    first_name = models.CharField(
        _('First Name'),
        max_length=50,
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=50,
    )
    email = models.EmailField(
        _('Email Address'),
        unique=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        help_text=_('Set your preferred language for the app')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def avatar(self):
        response = get_gravatar_url(self.email, size=80)
        return response

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

    def get_absolute_url(self):
        return '/users/{uuid}/'.format(uuid=self.uuid)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    @classmethod
    def get_class_name(cls):
        value = cls.__name__.lower()
        return value

    class Meta:
        ordering = ['email', 'created_on']
        verbose_name = _('User Account')
        verbose_name_plural = _('User Accounts')

    @models.permalink
    def get_absolute_url(self):
        return 'account_detail', [self.uuid]

    def __unicode__(self):
        return self.email


class AccountProxyBase(Account):
    """A proxy object so we can treat different users types distinctly.

    Heavily used in the admin to customize how user accounts
    are managed from there.
    """

    class Meta:
        proxy = True

    def __unicode__(self):
        return self.email


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
