from django.contrib import admin
from openbudgets.apps.pages.models import Page


class PageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Page, PageAdmin)
