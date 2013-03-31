from modeltranslation.translator import translator, TranslationOptions
from openbudget.apps.entities.models import Entity


class EntityTransOps(TranslationOptions):
    fields = ('name', 'slug')


translator.register(Entity, EntityTransOps)
