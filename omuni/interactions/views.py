from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from omuni.interactions.models import Remark
from django.contrib.comments.feeds import LatestCommentFeed


class CommentFeed(Feed):
    """"Give an object, get all comments for it as Atom"""
    feed_type = Atom1Feed

    def get_object(self, request, model, uuid):

        content_type = ContentType.objects.get(model=model)
        module_name, class_name = content_type.app_label, content_type.model

        obj = get_model(module_name, class_name)

        return get_object_or_404(
            obj,
            uuid=uuid
        )

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
        value = ''
        return value
