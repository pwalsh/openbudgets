from django.views.generic import TemplateView, DetailView, FormView
from django.http import HttpResponse
from openbudget.apps.pages.models import Page
from openbudget.apps.pages.forms import ContactForm


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # Add to the home context here.
        return context


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'

    def form_invalid(self, form, request=None):

        response = super(ContactView, self).form_invalid(form)

        if self.request.is_ajax():

            # we are simplifying the errors because of the available UI space.

            if 'email' in dict(form.errors):

                chosen_error = form.errors['email'][0]

            elif 'name' in dict(form.errors):

                chosen_error = form.errors['name'][0]

            else:

                chosen_error = form.errors['__all__'][0]

            data = chosen_error

            # JQuery is expecting a string, not an object.
            #return self.render_to_json_response(data, status=400)
            return HttpResponse(data)

        else:

            return response

    def form_valid(self, request, form):

        response = super(ContactView, self).form_valid(request, form)

        if self.request.is_ajax():
            data = {
                'data': _('Check your email to proceed'),
            }

            return self.render_to_json_response(data)

        else:

            return response


class PageView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'
