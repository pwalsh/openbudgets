from modeltranslation.translator import translator, TranslationOptions
from openbudget.apps.budgets.models import Budget, BudgetItem, Actual, ActualItem, Template, TemplateNode

class SheetTransOps(TranslationOptions):
    fields = ('description',)

class SheetItemTransOps(TranslationOptions):
    fields = ('description',)

class TemplateTransOps(TranslationOptions):
    fields = ('name', 'description')

class TemplateNodeTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(Budget, SheetTransOps)
translator.register(BudgetItem, SheetItemTransOps)
translator.register(Actual, SheetTransOps)
translator.register(ActualItem, SheetItemTransOps)
translator.register(Template, TemplateTransOps)
translator.register(TemplateNode, TemplateNodeTransOps)
