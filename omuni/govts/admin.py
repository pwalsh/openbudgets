from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from omuni.govts.models import GeoPoliticalEntity
from omuni.commons.admin import TranslatedMedia


class GeoPoliticalEntityAdmin(TranslationAdmin):

    Media = TranslatedMedia


admin.site.register(GeoPoliticalEntity, GeoPoliticalEntityAdmin)
