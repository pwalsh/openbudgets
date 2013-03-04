from modeltranslation.translator import translator, TranslationOptions
from openbudget.govts.models import GeoPoliticalEntity


class GeoPoliticalEntityTransOps(TranslationOptions):
    fields = ('name', 'slug')


translator.register(GeoPoliticalEntity, GeoPoliticalEntityTransOps)
