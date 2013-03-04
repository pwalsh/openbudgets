from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from openbudget.govts.models import GeoPoliticalEntity
from openbudget.commons.admin import TranslatedMedia


class GeoPoliticalEntityAdmin(TranslationAdmin):

    Media = TranslatedMedia


admin.site.register(GeoPoliticalEntity, GeoPoliticalEntityAdmin)
