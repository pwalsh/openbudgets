from modeltranslation.translator import translator, TranslationOptions
from openbudget.apps.sources.models import ReferenceSource, AuxSource


class ReferenceSourceTransOps(TranslationOptions):
    fields = ('name', 'notes')


class AuxSourceTransOps(TranslationOptions):
    fields = ('name', 'notes')


translator.register(ReferenceSource, ReferenceSourceTransOps)
translator.register(AuxSource, AuxSourceTransOps)
