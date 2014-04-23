from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from openbudgets.apps.entities.models import Entity


class EntityAdmin(TranslationAdmin):
    pass


admin.site.register(Entity, EntityAdmin)
