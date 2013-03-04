from django.views.generic import TemplateView, DetailView, FormView
from openbudget.pages.models import Page
from openbudget.pages.forms import ContactForm


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # Add to the home context here.
        return context


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'


class PageView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'
