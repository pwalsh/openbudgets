from modeltranslation.translator import translator, TranslationOptions
from omuni.budgets.models import Budget, BudgetItem, BudgetClassificationTree, BudgetClassificationTreeNode 

class BudgetTransOps(TranslationOptions):
    fields = ('description',)

class BudgetItemTransOps(TranslationOptions):
    fields = ('explanation',)

class BudgetClassificationTreeTransOps(TranslationOptions):
    fields = ('name',)

class BudgetClassificationTreeNodeTransOps(TranslationOptions):
    fields = ('name', 'description')


translator.register(Budget, BudgetTransOps)
translator.register(BudgetItem, BudgetItemTransOps)
translator.register(BudgetClassificationTree, BudgetClassificationTreeTransOps)
translator.register(BudgetClassificationTreeNode, BudgetClassificationTreeNodeTransOps)