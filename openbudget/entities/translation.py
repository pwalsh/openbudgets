from modeltranslation.translator import translator, TranslationOptions
from openbudget.entities.models import Entity


class EntityTransOps(TranslationOptions):
    fields = ('name', 'slug')


translator.register(Entity, EntityTransOps)
