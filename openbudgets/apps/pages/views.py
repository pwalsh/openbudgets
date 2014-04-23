from django.views.generic import TemplateView, DetailView, FormView
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from openbudgets.apps.pages.models import Page
from openbudgets.apps.pages.forms import ContactForm
from openbudgets.commons.mixins.views import JSONResponseMixin


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # Add to the home context here.
        return context


class ContactView(JSONResponseMixin, FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'
    success_url = '/contact/'

    def form_invalid(self, form, *args, **kwargs):

        response = super(ContactView, self).form_invalid(form)

        if self.request.is_ajax():

            # we are simplifying the errors because of the available UI space.

            if 'email' in dict(form.errors):

                chosen_error = form.errors['email'][0]

            elif 'name' in dict(form.errors):

                chosen_error = form.errors['name'][0]

            elif 'message' in dict(form.errors):

                chosen_error = form.errors['message'][0]

            else:

                chosen_error = form.errors['__all__'][0]

            data = chosen_error

            # JQuery is expecting a string, not an object.
            #return self.render_to_json_response(data, status=400)
            return HttpResponse(data)

        else:

            return response

    def form_valid(self, form, *args, **kwargs):

        response = super(ContactView, self).form_valid(form)

        if self.request.is_ajax():

            data = {'data': _('Success'), 'next': self.request.POST['next']}

            return self.render_to_json_response(data)

        else:

            return response


class PageView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'
