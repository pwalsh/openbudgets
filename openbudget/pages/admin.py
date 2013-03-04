from django.contrib import admin
from openbudget.pages.models import Page
from grappelli_modeltranslation.admin import TranslationAdmin


class PageAdmin(TranslationAdmin):
    pass


admin.site.register(Page, PageAdmin)
