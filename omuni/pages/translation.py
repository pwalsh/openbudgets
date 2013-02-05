from modeltranslation.translator import translator, TranslationOptions
from omuni.pages.models import Page

class PageTransOps(TranslationOptions):
    fields = ('title', 'slug', 'content')


translator.register(Page, PageTransOps)