from django.views.generic import DetailView, UpdateView
from braces.views import LoginRequiredMixin
from openbudget.apps.accounts.models import Account
from openbudget.apps.accounts.forms import AccountNameForm, AccountForm
from openbudget.commons.mixins.views import UserDataObjectMixin


class AccountDetailView(LoginRequiredMixin, UserDataObjectMixin, DetailView):
    model = Account
    template_name = 'accounts/account_detail.html'
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context['name_form'] = AccountNameForm(instance=self.request.user)
        return context


class AccountUpdateView(LoginRequiredMixin, UserDataObjectMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_update.html'
    slug_field = 'uuid'
