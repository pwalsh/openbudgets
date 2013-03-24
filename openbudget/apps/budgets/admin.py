from django.contrib import admin
from grappelli_modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem
from openbudget.apps.sources.admin import DataSourceInline


class BudgetTemplaeNodeAdmin(TranslationAdmin):
    """Admin form for adding budget template nodes"""

    filter_horizontal = ('templates',)


class BudgetTemplateAdmin(TranslationAdmin):
    """Admin form for adding budget templates"""

    inlines = [DataSourceInline,]


class BudgetItemInline(TranslationStackedInline):
    """Gives an inlineable BudgetItem form"""

    model = BudgetItem
    fk_name = 'budget'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2


class BudgetAdmin(TranslationAdmin):
    """Admin form for adding budgets"""

    inlines = [DataSourceInline, BudgetItemInline]


class ActualItemInline(TranslationStackedInline):
    """Gives an inlineable ActualItem form"""

    model = ActualItem
    fk_name = 'actual'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2


class ActualAdmin(TranslationAdmin):
    """Admin form for adding actuals"""

    inlines = [ActualItemInline, DataSourceInline]


admin.site.register(BudgetTemplate, BudgetTemplateAdmin)
admin.site.register(BudgetTemplateNode, BudgetTemplaeNodeAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Actual, ActualAdmin)
