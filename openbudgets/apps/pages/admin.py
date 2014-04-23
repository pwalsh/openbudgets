from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from openbudgets.apps.pages.models import Page


class PageAdmin(TranslationAdmin):
    pass


admin.site.register(Page, PageAdmin)
