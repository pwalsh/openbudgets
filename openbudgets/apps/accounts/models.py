from itertools import chain
from django.conf import settings
from django.db import models
from django.db.models.loading import get_model
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from openbudgets.apps.interactions.models import Star, Follow
from openbudgets.commons.mixins import models as mixins
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


class Account(mixins.UUIDMixin, mixins.TimeStampMixin, PermissionsMixin,
              AbstractBaseUser, mixins.ClassMethodMixin):

    """Extends Django's User with Open Budgets' specific user fields."""

    class Meta:
        ordering = ['email', 'created_on']
        verbose_name = _('User Account')
        verbose_name_plural = _('User Accounts')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AccountManager()

    first_name = models.CharField(
        _('First Name'),
        max_length=50,)

    last_name = models.CharField(
        _('Last Name'),
        max_length=50,)

    email = models.EmailField(
        _('Email Address'),
        unique=True,)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'),)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'),)

    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        help_text=_('Set your preferred language for the app'),)

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

    def get_full_name(self):
        full_name = '{first} {last}'.format(first=self.first_name,
                                            last=self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def get_absolute_url(self):
        return reverse('account_detail', [self.uuid])

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
        return super(CoreTeamAccountManager, self).get_queryset().filter(
            groups=settings.OPENBUDGETS_GROUP_ID_CORE)


class CoreTeamAccount(AccountProxyBase):

    """Provides a proxy interface to users on the core team"""

    class Meta:
        proxy = True
        verbose_name = _('Core team user')
        verbose_name_plural = _('Core team users')

    objects = CoreTeamAccountManager()

    def save(self, *args, **kwargs):
        super(CoreTeamAccount, self).save(*args, **kwargs)
        self.groups.add(settings.OPENBUDGETS_GROUP_ID_CORE)


class ContentTeamAccountManager(models.Manager):

    """Filter content team user proxy queries correctly"""

    def get_query_set(self):
        return super(ContentTeamAccountManager, self).get_queryset().filter(
            groups=settings.OPENBUDGETS_GROUP_ID_CONTENT)


class ContentTeamAccount(AccountProxyBase):

    """Provides a proxy interface to users on the content team"""

    class Meta:
        proxy = True
        verbose_name = _('Content team user')
        verbose_name_plural = _('Content team users')

    objects = ContentTeamAccountManager()

    def save(self, *args, **kwargs):
        super(ContentTeamAccount, self).save(*args, **kwargs)
        self.groups.add(settings.OPENBUDGETS_GROUP_ID_CONTENT)


class PublicAccountManager(models.Manager):
    """Filter public user proxy queries correctly"""

    def get_query_set(self):
        return super(PublicAccountManager, self).get_queryset().filter(
            groups=settings.OPENBUDGETS_GROUP_ID_PUBLIC)


class PublicAccount(AccountProxyBase):
    """Provides a proxy interface to public users"""

    class Meta:
        proxy = True
        verbose_name = _('Public user')
        verbose_name_plural = _('Public users')

    objects = PublicAccountManager()

    def save(self, *args, **kwargs):
        super(PublicAccount, self).save(*args, **kwargs)
        self.groups.add(settings.OPENBUDGETS_GROUP_ID_PUBLIC)
