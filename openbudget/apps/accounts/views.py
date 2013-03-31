from django.views.generic import DetailView, UpdateView
from braces.views import LoginRequiredMixin
from openbudget.apps.accounts.models import UserProfile
from openbudget.apps.accounts.forms import UserProfileForm
from openbudget.commons.mixins.views import UserDataObjectMixin


class UserProfileDetailView(LoginRequiredMixin, UserDataObjectMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/user_profile_detail.html'
    slug_field = 'uuid'


class UserProfileUpdateView(LoginRequiredMixin, UserDataObjectMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/user_profile_update.html'
    slug_field = 'uuid'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(UserProfileUpdateView, self).get_form_kwargs(**kwargs)

        data = {
            'username': self.object.user.username,
            'email': self.object.user.email,
            'first_name': self.object.user.first_name,
            'last_name': self.object.user.last_name,
            'language': self.object.language
        }

        kwargs.update({'initial': data})
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        user = self.object.user
        user.username = form.cleaned_data.get('username')
        user.email = form.cleaned_data.get('email')
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        self.object.save()

        return super(UserProfileUpdateView, self).form_valid(form)
