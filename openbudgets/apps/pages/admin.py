from django.db import models
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from redactor.widgets import AdminRedactorEditor
from openbudgets.apps.pages.models import Page


class PageAdmin(TranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminRedactorEditor},
    }


admin.site.register(Page, PageAdmin)
