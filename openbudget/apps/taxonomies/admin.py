from django.contrib import admin
from openbudget.apps.taxonomies.models import Taxonomy, TaxonomyTag, TaxonomyTaggedItem
from taggit.models import Tag


admin.site.unregister(Tag)
admin.site.register(Taxonomy)
admin.site.register(TaxonomyTag)
admin.site.register(TaxonomyTaggedItem)
