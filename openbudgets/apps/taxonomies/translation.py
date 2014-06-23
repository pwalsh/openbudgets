from modeltranslation.translator import translator, TranslationOptions
from openbudgets.apps.taxonomies import models


class TaxonomyTransOps(TranslationOptions):
    fields = ('name', 'description')


class TagTransOps(TranslationOptions):
    fields = ('name',)


translator.register(models.Taxonomy, TaxonomyTransOps)
translator.register(models.Tag, TagTransOps)
