from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from openbudgets.apps.sheets.models import Template, Sheet, SheetItem


class TemplateAdmin(TranslationAdmin):
    """Admin form for adding budget templates"""


class SheetItemInline(TranslationStackedInline):
    """Gives an inlineable BudgetItem form"""

    model = SheetItem
    fk_name = 'sheet'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2


class SheetAdmin(TranslationAdmin):
    """Admin form for adding budgets"""

    inlines = [SheetItemInline]


admin.site.register(Template, TemplateAdmin)
admin.site.register(Sheet, SheetAdmin)
