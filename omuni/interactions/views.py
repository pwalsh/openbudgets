from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _
from django.contrib import comments


class CommentFeed(Feed):
    """"Give an object, get all comments for it as Atom"""

    def get_object(self, request, q_id):
        pass
        #return get_object_or_404(
        #    DYNAMICALLY_GET_OBJECT_FROM_MODEL,
        #    pk=q_id
        #)

    def title(self, obj):
        return obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def subtitle(self, obj):
        return obj.description

    def items(self, obj):
        return obj.comments
