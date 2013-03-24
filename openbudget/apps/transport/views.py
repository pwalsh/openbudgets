from django.views.generic import View, FormView, TemplateView
from django.shortcuts import redirect
from openbudget.apps.transport.forms import FileImportForm
from openbudget.apps.transport.incoming import DataImporter
from openbudget.commons.mixins.views import FileResponseMixin
from openbudget.apps.budgets.models import Budget, Actual, BudgetItem, ActualItem


class DataImportView(FormView):
    form_class = FileImportForm
    template_name = 'transport/file_import.html'

    def form_valid(self, form, *args, **kwargs):
        sourcefile = self.request.FILES['sourcefile']
        importer = DataImporter(
            sourcefile,
            dataset_meta_in_filename=True
        )
        dataset = importer.dataset()
        response = importer.validate(dataset)
        if not response['valid']:
            return response
        save = importer.save(dataset)
        if save:
            return redirect('import_success')
        else:
            return 'SAVE FAILED'


class ImportSuccessView(TemplateView):
    template_name = 'transport/import_success.html'


class DataExportView(FileResponseMixin, View):
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
