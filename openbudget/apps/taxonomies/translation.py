from modeltranslation.translator import translator, TranslationOptions
from openbudget.apps.taxonomies.models import Taxonomy, Tag


class TaxonomyTransOps(TranslationOptions):
    fields = ('name', 'description')


class TagTransOps(TranslationOptions):
    fields = ('name',)


translator.register(Taxonomy, TaxonomyTransOps)
translator.register(Tag, TagTransOps)
