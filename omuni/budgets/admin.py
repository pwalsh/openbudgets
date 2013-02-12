from django.contrib import admin
from omuni.budgets.models import BudgetClassificationTree, BudgetClassificationTreeNode, Budget, BudgetItem


admin.site.register(BudgetClassificationTree)
admin.site.register(BudgetClassificationTreeNode)
admin.site.register(Budget)
admin.site.register(BudgetItem)
