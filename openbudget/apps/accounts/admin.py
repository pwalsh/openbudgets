from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from registration.models import RegistrationProfile
from openbudget.settings import base as settings
from openbudget.apps.accounts.models import Account, PublicAccount, ContentTeamAccount, \
    CoreTeamAccount
from openbudget.apps.accounts.forms import AccountCreationForm, \
    AccountChangeForm


class AccountAdmin(UserAdmin):
    """Defines common settings for all our UserProxy forms"""

    form = AccountChangeForm
    add_form = AccountCreationForm
    fieldsets = (
        (_('Account credentials'), {'fields': ('password', 'email', 'first_name', 'last_name', 'is_active')}),
    )


class CoreTeamAccountAdmin(AccountAdmin):
    """Admin form for Core Team members"""

    def queryset(self, request):
        core_team_users = Group.objects.filter(id=settings.OPENBUDGET_CORE_TEAM_ID)
        qs = super(CoreTeamAccountAdmin, self).queryset(request)
        qs = qs.filter(groups=core_team_users)
        return qs


class ContentTeamAccountAdmin(AccountAdmin):
    """Admin form for Content Team members"""

    def queryset(self, request):
        content_team_users = Group.objects.filter(id=settings.OPENBUDGET_CONTENT_TEAM_ID)
        qs = super(ContentTeamAccountAdmin, self).queryset(request)
        qs = qs.filter(groups=content_team_users)
        return qs


class PublicAccountAdmin(AccountAdmin):
    """Admin form for Public users"""

    def queryset(self, request):
        public_users = Group.objects.filter(id=settings.OPENBUDGET_PUBLIC_ID)
        qs = super(PublicAccountAdmin, self).queryset(request)
        qs = qs.filter(groups=public_users)
        return qs


# Django Auth admin config
admin.site.unregister(Group)

# Django Sites admin config
admin.site.unregister(Site)

# Registration admin config
admin.site.unregister(RegistrationProfile)

# Open Budget Accounts admin config
#admin.site.register(CoreTeamAccount, CoreTeamAccountAdmin)
#admin.site.register(ContentTeamAccount, ContentTeamAccountAdmin)
#admin.site.register(PublicAccount, PublicAccountAdmin)
