from django import template
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from openbudget.interactions.models import Star


register = template.Library()


@register.inclusion_tag('interactions/partials/_star.html')
def star(obj, user):
    """Returns a star"""

    if not user.is_authenticated():
        # do something
        return None
    else:
        content_type = ContentType.objects.get(model=obj.get_class_name())
        data = {
            'user': user,
            'content_type': obj.get_class_name(),
            'object_id': obj.id,
        }

        try:
            star = Star.objects.get(user=user, content_type=content_type)
            data['star'] = '&#9733;'
            data['title'] = _('Unstar this item')
            data['obj'] = star.id

        except Star.DoesNotExist:
            data['star'] = '&#9734;'
            data['title'] = _('Star this item')

        return data
