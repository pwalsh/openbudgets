from django.views.generic import DetailView
from braces.views import LoginRequiredMixin
from omuni.accounts.models import UserProfile


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/user_profile_detail.html'
    slug_field = 'uuid'
