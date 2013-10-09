from modeltranslation.translator import translator, TranslationOptions
from openbudgets.apps.pages.models import Page


class PageTransOps(TranslationOptions):
    fields = ('title', 'content')


translator.register(Page, PageTransOps)
