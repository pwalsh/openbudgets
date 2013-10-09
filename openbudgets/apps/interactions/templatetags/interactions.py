from django import template
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from openbudgets.apps.interactions.models import Star, Follow


register = template.Library()


@register.inclusion_tag('interactions/partials/_star.html')
def star(obj, user):
    """Returns a star form"""

    if not user.is_authenticated():
        # do something
        return None
    else:
        content_type = ContentType.objects.get(
            model=obj.get_class_name()
        )
        data = {
            'user': user,
            'content_type': obj.get_class_name(),
            'object_id': obj.id,
        }

        try:
            star = Star.objects.get(
                user=user,
                content_type=content_type,
                object_id=obj.id
            )
            data['interaction'] = Star.get_class_name()
            data['star'] = _('Unstar') + ' ' + '&#9733;'
            data['title'] = _('Unstar this item')
            data['obj'] = star.id

        except Star.DoesNotExist:
            data['interaction'] = Star.get_class_name()
            data['star'] = _('Star') + ' ' + '&#9734;'
            data['title'] = _('Add this item to your starred items for future reference.')

        return data


@register.inclusion_tag('interactions/partials/_follow.html')
def follow(obj, user):
    """Returns a follow form"""

    if not user.is_authenticated():
        # do something
        return None
    else:
        content_type = ContentType.objects.get(
            model=obj.get_class_name()
        )
        data = {
            'user': user,
            'content_type': obj.get_class_name(),
            'object_id': obj.id,
        }

        try:
            follow = Follow.objects.get(
                user=user,
                content_type=content_type,
                object_id=obj.id
            )
            data['interaction'] = Follow.get_class_name()
            data['follow'] = _('Unfollow') + ' ' + '&#10058;'
            data['title'] = _('Unfollow this item')
            data['obj'] = follow.id

        except Follow.DoesNotExist:
            data['interaction'] = Follow.get_class_name()
            data['follow'] = _('Follow') + ' ' + '&#10058;'
            data['title'] = _('Add this item to your followed items. You will receive email for any updates or discussion on the item.')

        return data
