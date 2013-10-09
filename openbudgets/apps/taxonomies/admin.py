from django.contrib import admin
from openbudgets.apps.taxonomies.models import Taxonomy, Tag, TaggedNode
from taggit.models import Tag as TaggitTag


admin.site.unregister(TaggitTag)
admin.site.register(Taxonomy)
admin.site.register(Tag)
admin.site.register(TaggedNode)
