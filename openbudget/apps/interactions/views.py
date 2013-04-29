from django.contrib.syndication.views import Feed
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.utils.feedgenerator import Atom1Feed
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404


class CommentFeed(Feed):
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
        value = obj.discussion.all()
        return value


def toggleable_interaction(request):
    """Post data and if it fits, we'll create or delete a toggleable interaction type"""
    data= request.POST
    content_type = ContentType.objects.get(
        model=data['content_type']
    )
    user = get_user_model().objects.get(
        id=data['user']
    )
    interaction = get_model(
        'interactions',
        data['interaction']
    )

    if 'obj' in data:
        intobj = interaction.objects.get(
            id=int(data['obj'])
        )
        intobj.delete()
    else:
        intobj = interaction.objects.create(
            user=user,
            content_type=content_type,
            object_id=int(data['object_id'])
        )

    obj_url= intobj.content_object.get_absolute_url()

    return HttpResponseRedirect(obj_url)

