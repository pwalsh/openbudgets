from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from registration.models import RegistrationProfile
from openbudget.apps.accounts.models import Account, PublicUserProxy, ContentTeamUserProxy, CoreTeamUserProxy


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
        qs = qs.filter(groups=core_team_user_group)
        return qs


class ContentTeamUserProxyAdmin(UserProxyBaseAdmin):
    """Admin form for Content Team members"""

    def queryset(self, request):
        content_team_user_group = Group.objects.filter(id=2)
        qs = super(ContentTeamUserProxyAdmin, self).queryset(request)
        qs = qs.filter(groups=content_team_user_group)
        return qs


class PublicUserProxyAdmin(UserProxyBaseAdmin):
    """Admin form for Public users"""

    def queryset(self, request):
        public_user_group = Group.objects.filter(id=3)
        qs = super(PublicUserProxyAdmin, self).queryset(request)
        qs = qs.filter(groups=public_user_group)
        return qs


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
