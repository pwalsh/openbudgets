from modeltranslation.translator import translator, TranslationOptions
from openbudget.budgets.models import Budget, BudgetItem, Actual, ActualItem, BudgetTemplate, BudgetTemplateNode 

class SheetTransOps(TranslationOptions):
    fields = ('description',)

class SheetItemTransOps(TranslationOptions):
    fields = ('description',)

class BudgetTemplateTransOps(TranslationOptions):
    fields = ('name',)

class BudgetTemplateNodeTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(Budget, SheetTransOps)
translator.register(BudgetItem, SheetItemTransOps)
translator.register(Actual, SheetTransOps)
translator.register(ActualItem, SheetItemTransOps)
translator.register(BudgetTemplate, BudgetTemplateTransOps)
translator.register(BudgetTemplateNode, BudgetTemplateNodeTransOps)