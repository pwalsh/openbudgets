from django.contrib import admin
from omuni.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem


class BudgetTemplateNodeInline(admin.StackedInline):
    """Gives an inlineable BudgetTemplateNode form"""

    model = BudgetTemplateNode
    fk_name = 'template'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 2


class BudgetTemplateAdmin(admin.ModelAdmin):
    """Admin form for adding budget templates"""

    inlines = [BudgetTemplateNodeInline]


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


admin.site.register(BudgetTemplate, BudgetTemplateAdmin)
admin.site.register(Budget, BudgetAdmin)
