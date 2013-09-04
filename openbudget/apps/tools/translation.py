from modeltranslation.translator import translator, TranslationOptions
from openbudget.apps.tools.models import Tool


class ToolTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(Tool, ToolTransOps)
