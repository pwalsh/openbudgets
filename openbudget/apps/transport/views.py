from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect
from openbudget.apps.transport.forms import FileImportForm
from openbudget.apps.transport.incoming import DataImporter


class FileImportView(FormView):
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
