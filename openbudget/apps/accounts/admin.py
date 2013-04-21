from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from registration.models import RegistrationProfile
from openbudget.apps.accounts.models import Account, PublicUserProxy, ContentTeamUserProxy, CoreTeamUserProxy


class AccountInline(admin.StackedInline):
    """Gives an inlineable Account form"""

    model = Account
    fk_name = 'user'
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    max_num = 1


class UserProxyBaseAdmin(UserAdmin):
    """Defines common settings for all our UserProxy forms"""

    fieldsets = (
        (_('Account credentials'), {'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'is_active')}),
    )


class CoreTeamUserProxyAdmin(UserProxyBaseAdmin):
    """Admin form for Core Team members"""

    def queryset(self, request):
        core_team_user_group = Group.objects.filter(id=1)
        qs = super(CoreTeamUserProxyAdmin, self).queryset(request)
        qs = qs.filter(groups__in=core_team_user_group)
        return qs

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(CoreTeamUserProxyAdmin, self).add_view(
            request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [AccountInline]
        return super(CoreTeamUserProxyAdmin, self).change_view(request, object_id, form_url, extra_context)


class ContentTeamUserProxyAdmin(UserProxyBaseAdmin):
    """Admin form for Content Team members"""

    def queryset(self, request):
        content_team_user_group = Group.objects.filter(id=2)
        qs = super(ContentTeamUserProxyAdmin, self).queryset(request)
        qs = qs.filter(groups__in=content_team_user_group)
        return qs

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(ContentTeamUserProxyAdmin, self).add_view(
            request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [AccountInline]
        return super(ContentTeamUserProxyAdmin, self).change_view(request, object_id, form_url, extra_context)


class PublicUserProxyAdmin(UserProxyBaseAdmin):
    """Admin form for Public users"""

    def queryset(self, request):
        public_user_group = Group.objects.filter(id=3)
        qs = super(PublicUserProxyAdmin, self).queryset(request)
        qs = qs.filter(groups__in=public_user_group)
        return qs

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(PublicUserProxyAdmin, self).add_view(
            request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [AccountInline]
        return super(PublicUserProxyAdmin, self).change_view(request, object_id, form_url, extra_context)


# Django Auth admin config
admin.site.unregister(Group)

# Django Sites admin config
admin.site.unregister(Site)

# Registration admin config
admin.site.unregister(RegistrationProfile)

# Open Budget Accounts admin config
admin.site.register(CoreTeamUserProxy, CoreTeamUserProxyAdmin)
admin.site.register(ContentTeamUserProxy, ContentTeamUserProxyAdmin)
admin.site.register(PublicUserProxy, PublicUserProxyAdmin)
