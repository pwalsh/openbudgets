from modeltranslation.translator import translator, TranslationOptions
from openbudget.apps.projects.models import Project


class ProjectTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(Project, ProjectTransOps)
