from modeltranslation.translator import translator, TranslationOptions
from openbudget.apps.entities.models import Domain, Division, Entity


class DomainTransOps(TranslationOptions):
    fields = ('name',)


class DivisionTransOps(TranslationOptions):
    fields = ('name',)


class EntityTransOps(TranslationOptions):
    fields = ('name', 'description')

translator.register(Domain, DomainTransOps)
translator.register(Division, DivisionTransOps)
translator.register(Entity, EntityTransOps)
