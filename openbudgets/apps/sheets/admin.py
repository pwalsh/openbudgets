from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from openbudgets.apps.sheets import models


class TemplateNodeAdmin(TranslationAdmin):
    """Gives a TemplateNode form"""


class TemplateAdmin(TranslationAdmin):
    """Admin form for adding templates"""


class SheetItemInline(TranslationStackedInline):
    """Gives an inlineable SheetItem form"""

    model = models.SheetItem
    fk_name = 'sheet'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)
    extra = 2


class SheetAdmin(TranslationAdmin):
    """Admin form for adding budgets"""

    inlines = [SheetItemInline]


admin.site.register(models.TemplateNode, TemplateNodeAdmin)
admin.site.register(models.Template, TemplateAdmin)
admin.site.register(models.Sheet, SheetAdmin)
