from modeltranslation.translator import translator, TranslationOptions
from openbudgets.apps.pages import models


class PageTransOps(TranslationOptions):
    fields = ('title', 'content')


translator.register(models.Page, PageTransOps)
