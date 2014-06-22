from modeltranslation.translator import translator, TranslationOptions
from openbudgets.apps.sources import models


class ReferenceSourceTransOps(TranslationOptions):
    fields = ('name', 'notes')


class AuxSourceTransOps(TranslationOptions):
    fields = ('name', 'notes')


translator.register(models.ReferenceSource, ReferenceSourceTransOps)
translator.register(models.AuxSource, AuxSourceTransOps)
