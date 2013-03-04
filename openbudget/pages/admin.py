from django.contrib import admin
from openbudget.pages.models import Page
from modeltranslation.admin import TranslationAdmin
from openbudget.commons.admin import TranslatedMedia


class PageAdmin(TranslationAdmin):

    Media = TranslatedMedia


admin.site.register(Page, PageAdmin)
