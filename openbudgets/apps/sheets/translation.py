from modeltranslation.translator import translator, TranslationOptions
from openbudgets.apps.sheets import models


class SheetTransOps(TranslationOptions):
    fields = ('description',)


class SheetItemTransOps(TranslationOptions):
    fields = ('name', 'description')


class TemplateTransOps(TranslationOptions):
    fields = ('name', 'description',)


class TemplateNodeTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(models.Sheet, SheetTransOps)
translator.register(models.SheetItem, SheetItemTransOps)
translator.register(models.Template, TemplateTransOps)
translator.register(models.TemplateNode, TemplateNodeTransOps)
