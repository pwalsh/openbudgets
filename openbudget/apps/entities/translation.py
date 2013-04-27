from modeltranslation.translator import translator, TranslationOptions
from openbudget.apps.entities.models import Domain, DomainDivision, Entity


class DomainTransOps(TranslationOptions):
    fields = ('name',)


class DomainDivisionTransOps(TranslationOptions):
    fields = ('name',)


class EntityTransOps(TranslationOptions):
    fields = ('name', 'description')

translator.register(Domain, DomainTransOps)
translator.register(DomainDivision, DomainDivisionTransOps)
translator.register(Entity, EntityTransOps)
