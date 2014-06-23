from modeltranslation.translator import translator, TranslationOptions
from openbudgets.apps.entities import models


class DomainTransOps(TranslationOptions):
    fields = ('name',)


class DivisionTransOps(TranslationOptions):
    fields = ('name',)


class EntityTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(models.Domain, DomainTransOps)
translator.register(models.Division, DivisionTransOps)
translator.register(models.Entity, EntityTransOps)
