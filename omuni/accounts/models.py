from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuidfield import UUIDField
from omuni.settings import LANGUAGES


class UserProfile(models.Model):
    """Extends Django's User with our project specific user fields"""

    uuid = UUIDField(
        auto=True
    )
    user = models.OneToOneField(
        User
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default='en',
        help_text=_('Set your prefered language for the app')
    )

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
