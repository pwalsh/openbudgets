from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from openbudget.budgets.models import BudgetTemplate, BudgetTemplateNode, Budget, BudgetItem, Actual, ActualItem
from openbudget.commons.admin import DataSourceInline
from openbudget.commons.admin import TranslatedMedia


class BudgetTemplateNodeInline(TranslationStackedInline):
    """Gives an inlineable BudgetTemplateNode form"""

    model = BudgetTemplateNode
    fk_name = 'template'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2
    Media = TranslatedMedia


class BudgetTemplateAdmin(TranslationAdmin):
    """Admin form for adding budget templates"""

    inlines = [DataSourceInline, BudgetTemplateNodeInline]
    Media = TranslatedMedia


class BudgetItemInline(TranslationStackedInline):
    """Gives an inlineable BudgetItem form"""

    model = BudgetItem
    fk_name = 'budget'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2
    Media = TranslatedMedia


class BudgetAdmin(TranslationAdmin):
    """Admin form for adding budgets"""

    inlines = [DataSourceInline, BudgetItemInline]
    Media = TranslatedMedia


class ActualItemInline(TranslationStackedInline):
    """Gives an inlineable ActualItem form"""

    model = ActualItem
    fk_name = 'actual'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2
    Media = TranslatedMedia


class ActualAdmin(TranslationAdmin):
    """Admin form for adding actuals"""

    inlines = [ActualItemInline, DataSourceInline]
    Media = TranslatedMedia


admin.site.register(BudgetTemplate, BudgetTemplateAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Actual, ActualAdmin)
