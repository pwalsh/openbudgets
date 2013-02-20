from django.contrib import admin
from omuni.pages.models import Page
from modeltranslation.admin import TranslationAdmin
from omuni.commons.admin import TranslatedMedia


class PageAdmin(TranslationAdmin):

    Media = TranslatedMedia


admin.site.register(Page, PageAdmin)
