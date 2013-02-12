from django.contrib import admin
from omuni.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem
from omuni.commons.admin import DataSourceInline


class BudgetTemplateNodeInline(admin.StackedInline):
    """Gives an inlineable BudgetTemplateNode form"""

    model = BudgetTemplateNode
    fk_name = 'template'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2


class BudgetTemplateAdmin(admin.ModelAdmin):
    """Admin form for adding budget templates"""

    inlines = [DataSourceInline, BudgetTemplateNodeInline]


class BudgetItemInline(admin.StackedInline):
    """Gives an inlineable BudgetItem form"""

    model = BudgetItem
    fk_name = 'budget'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2


class BudgetAdmin(admin.ModelAdmin):
    """Admin form for adding budgets"""

    inlines = [DataSourceInline, BudgetItemInline]


class ActualItemInline(admin.StackedInline):
    """Gives an inlineable ActualItem form"""

    model = ActualItem
    fk_name = 'actual'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2


class ActualAdmin(admin.ModelAdmin):
    """Admin form for adding actuals"""

    inlines = [ActualItemInline, DataSourceInline]


admin.site.register(BudgetTemplate, BudgetTemplateAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Actual, ActualAdmin)
