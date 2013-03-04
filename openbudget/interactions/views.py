from django.contrib.syndication.views import Feed
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from openbudget.interactions.models import Star


class ICommentFeed(Feed):
    """"Give an object, get all comments for it in Atom"""

    feed_type = Atom1Feed

    def get_object(self, request, model, uuid):

        # yeah, this might seem a convoluted way to get the obj
        # I know. I prefer it to a solution with getattr from the
        # model string. Got a better idea?
        content_type = ContentType.objects.get(model=model)
        module_name, class_name = content_type.app_label, content_type.model
        obj = get_model(module_name, class_name)

        return get_object_or_404(obj, uuid=uuid)

    def title(self, obj):
        value = obj.name
        return value

    def subtitle(self, obj):
        value = obj.description
        return value

    def link(self, obj):
        value = obj.get_absolute_url()
        return value

    def items(self, obj):
        value = obj.posts.all()
        return value


def toggleable_interaction(request):
    """Post data and if it fits, we'll create or delete a toggleable interaction type"""
    data= request.POST
    content_type = ContentType.objects.get(model=data['content_type'])
    user = User.objects.get(id=data['user'])
    if 'obj' in data.keys():

        star = Star.objects.get(id=int(data['obj']))
        star.delete()

    else:

        star = Star.objects.create(
            user=user,
            content_type=content_type,
            object_id=int(data['object_id'])
        )

    return HttpResponse('did it')

