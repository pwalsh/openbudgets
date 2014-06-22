from modeltranslation.translator import translator, TranslationOptions
from openbudgets.apps.tools import models


class ToolTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(models.Tool, ToolTransOps)
