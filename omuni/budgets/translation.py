from modeltranslation.translator import translator, TranslationOptions
from omuni.budgets.models import Budget, BudgetItem, BudgetTemplate, BudgetTemplateNode 

class BudgetTransOps(TranslationOptions):
    fields = ('description',)

class BudgetItemTransOps(TranslationOptions):
    fields = ('explanation',)

class BudgetTemplateTransOps(TranslationOptions):
    fields = ('name',)

class BudgetTemplateNodeTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(Budget, BudgetTransOps)
translator.register(BudgetItem, BudgetItemTransOps)
translator.register(BudgetTemplate, BudgetTemplateTransOps)
translator.register(BudgetTemplateNode, BudgetTemplateNodeTransOps)