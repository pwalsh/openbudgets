import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, Http404
from django.views.generic import View, FormView, TemplateView
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from braces.views import LoginRequiredMixin
from openbudgets.apps.transport.forms import FileImportForm
from openbudgets.apps.transport.incoming.importers.tablibimporter import TablibImporter
from openbudgets.apps.transport.tasks import save_import
from openbudgets.commons.mixins.views import FileResponseMixin
from openbudgets.apps.sheets.models import Sheet, SheetItem


class FileImportView(LoginRequiredMixin, FormView):

    """Takes data in a supported file format, extracts meta data from POST or
    the filename, and passes the payload to the appropriate parser for
    processing.

    All of Open Budgets' file-based data imports go through this view.

    If the view is accessed directly via a url, the user can choose and upload
    a file, where the meta data is extractable from the filename (see the docs).

    Otherwise, the view takes AJAX requests which minimally contain a file and
    meta data in the POST object.

    """

    form_class = FileImportForm
    template_name = 'transport/file_import.html'

    def form_valid(self, form, *args, **kwargs):

        # all we've done is validate that the form is validly formed.
        # This has nothing to do with the actual data import being valid.
        sourcefile = self.request.FILES['sourcefile']
        post_data = self.request.POST.copy()
        meta_from_filename = True

        if 'type' in post_data and 'attributes' in post_data:
            meta_from_filename = False

        importer = TablibImporter(sourcefile, post_data, meta_from_filename)
        valid, errors = importer.validate()

        if not valid:
            error_dicts = [e.to_json() for e in errors]
            return HttpResponseBadRequest(json.dumps(error_dicts), content_type='application/json')

        if self.request.is_ajax():
            save_import.apply_async((importer.deferred(), self.request.user.email))
            return HttpResponse(u'OK')
        else:
            #save = importer.save()
            save = save_import.apply_async((importer.deferred(), self.request.user.email))
            if save:
                return redirect('import_success')
            else:
                return HttpResponseServerError(_(u'Save failed.'))


class FileExportView(FileResponseMixin, View):
    """Export Budget or Actual data in a supported format."""

    def get_context_data(self, **kwargs):
        context = {'params': kwargs}
        if self.kwargs['model'] == 'sheet':
            try:
                pk = self.kwargs['pk']
                obj = Sheet.objects.get(pk=pk)
                obj_list = SheetItem.objects.filter(sheet=obj)
            except Sheet.DoesNotExist:
                raise Http404(_("No sheets found for pk: {pk}").format(pk=pk))
        else:
            # export other stuff
            obj = {}
            obj_list = []

        context['object'] = obj
        context['object_list'] = obj_list

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ImportSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'transport/import_success.html'


class ImportAppView(LoginRequiredMixin, TemplateView):
    template_name = 'transport/importer.html'

    def get_context_data(self, **kwargs):
        context = super(ImportAppView, self).get_context_data(**kwargs)
        context['UPLOAD_URL'] = reverse('data_import')

        return context
