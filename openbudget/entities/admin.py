from django.contrib import admin
from grappelli_modeltranslation.admin import TranslationAdmin
from openbudget.entities.models import Entity


class EntityAdmin(TranslationAdmin):
    pass

admin.site.register(Entity, EntityAdmin)
