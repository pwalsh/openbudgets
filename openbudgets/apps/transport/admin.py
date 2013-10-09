from django.contrib import admin
from openbudgets.apps.transport.models import String


class StringInline(admin.StackedInline):
    """Gives an inlineable String form"""

    model = String
    fk_name = 'parent'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 1


class StringAdmin(admin.ModelAdmin):
    inlines = [StringInline]

    def queryset(self, request):
        qs = super(StringAdmin, self).queryset(request)
        qs = qs.filter(parent__isnull=True)
        return qs


admin.site.register(String, StringAdmin)
