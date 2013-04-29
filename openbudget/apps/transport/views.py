import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.views.generic import View, FormView, TemplateView
from django.shortcuts import redirect
from django.shortcuts import render
from openbudget.apps.transport.forms import FileImportForm
from openbudget.apps.transport.incoming.importers import TablibImporter
from openbudget.apps.transport.tasks import save_import
from openbudget.commons.mixins.views import FileResponseMixin
from openbudget.apps.budgets.models import Budget, Actual, BudgetItem, ActualItem


class FileImportView(FormView):
    """View to import from file, where metadata is in the filename.

    This view is a simple import interface targeted mainly at
    developers who do not want to work with the full importer form.
    """
    form_class = FileImportForm
    template_name = 'transport/file_import.html'

    def form_valid(self, form, *args, **kwargs):
        use_filename = True
        sourcefile = self.request.FILES['sourcefile']
        post_data = self.request.POST.copy()

        if 'type' in post_data and 'attributes' in post_data:
            use_filename = False

        importer = TablibImporter(
            sourcefile,
            post_data,
            dataset_meta_in_filename=use_filename
        )
        valid, errors = importer.validate()
        if not valid:
            error_dicts = [e.__dict__() for e in errors]
            return HttpResponseBadRequest(json.dumps(error_dicts), content_type='application/json')

        if self.request.is_ajax():
            save_import.apply_async((importer.deferred(), self.request.user.email))
            return HttpResponse('OK')
        else:
            save = importer.save()
            if save:
                return redirect('import_success')
            else:
                return HttpResponseServerError('SAVE FAILED')


class FileExportView(FileResponseMixin, View):
    """Export Budget or Actual data in a supported format."""

    def get_context_data(self, **kwargs):
        context = {}
        context['params'] = kwargs
        if self.kwargs['model'] == 'budget':
            obj = Budget.objects.get(uuid=self.kwargs['uuid'])
            obj_list = BudgetItem.objects.filter(budget=obj)
        elif self.kwargs['model'] == 'actual':
            obj = Actual.objects.get(uuid=self.kwargs['uuid'])
            obj_list = ActualItem.objects.filter(actual=obj)
        context['object'] = obj
        context['object_list'] = obj_list
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ImportSuccessView(TemplateView):
    template_name = 'transport/import_success.html'


def importer_app(request):
    return render(request, 'transport/importer.html', {
        'UPLOAD_URL': reverse('data_import')
    })
