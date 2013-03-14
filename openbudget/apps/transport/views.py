from django.views.generic import FormView
from openbudget.apps.transport.forms import FileImportForm
from openbudget.apps.transport.incoming import FileImporter


class FileImportView(FormView):
    form_class = FileImportForm
    template_name = 'transport/file_import.html'

    def form_valid(self, form, *args, **kwargs):
        sourcefile = self.request.FILES['sourcefile']
        importer = FileImporter(sourcefile)
        name, datatype, divisions = importer.get_metadata()
        dataset = importer.create_dataset()
        dataset = importer.normalize_headers(dataset)
