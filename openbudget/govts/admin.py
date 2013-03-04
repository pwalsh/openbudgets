from django.contrib import admin
from grappelli_modeltranslation.admin import TranslationAdmin
from openbudget.govts.models import GeoPoliticalEntity


class GeoPoliticalEntityAdmin(TranslationAdmin):
    pass

admin.site.register(GeoPoliticalEntity, GeoPoliticalEntityAdmin)
