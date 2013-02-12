from django.contrib import admin
from omuni.budgets.models import BudgetClassificationTree, BudgetClassificationTreeNode, Budget, BudgetItem


class BudgetClassificationTreeNodeInline(admin.StackedInline):
    """Gives an inlineable BudgetClassificationTreeNode form"""

    model = BudgetClassificationTreeNode
    fk_name = 'tree'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 2


class BudgetClassificationTreeAdmin(admin.ModelAdmin):
    """Admin form for adding budget classification trees"""

    inlines = [BudgetClassificationTreeNodeInline]


class BudgetItemInline(admin.StackedInline):
    """Gives an inlineable BudgetItem form"""

    model = BudgetItem
    fk_name = 'budget'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 2


class BudgetAdmin(admin.ModelAdmin):
    """Admin form for adding budgets"""

    inlines = [BudgetItemInline]


admin.site.register(BudgetClassificationTree, BudgetClassificationTreeAdmin)
admin.site.register(Budget, BudgetAdmin)
