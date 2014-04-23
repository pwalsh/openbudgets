from django.contrib import admin
from openbudgets.apps.entities.models import Entity


class EntityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Entity, EntityAdmin)
