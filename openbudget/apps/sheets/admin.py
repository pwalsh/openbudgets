from django.contrib import admin
from grappelli_modeltranslation.admin import TranslationAdmin, \
    TranslationStackedInline
from openbudget.apps.sheets.models import Template, Sheet, SheetItem
from openbudget.apps.sources.admin import ReferenceSourceInline, AuxSourceInline


class TemplateAdmin(TranslationAdmin):
    """Admin form for adding budget templates"""

    inlines = [ReferenceSourceInline, AuxSourceInline]


class SheetItemInline(TranslationStackedInline):
    """Gives an inlineable BudgetItem form"""

    model = SheetItem
    fk_name = 'sheet'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2


class SheetAdmin(TranslationAdmin):
    """Admin form for adding budgets"""

    inlines = [SheetItemInline, ReferenceSourceInline, AuxSourceInline]


admin.site.register(Template, TemplateAdmin)
admin.site.register(Sheet, SheetAdmin)
