import datetime
import json
import tablib
from django.core.exceptions import PermissionDenied
from django import http
from django.views.generic.detail import SingleObjectMixin


class UserDataObjectMixin(SingleObjectMixin):
    """Returns a data object only if it belongs to the request user.

    This mixin is only for use with objects that have a foreign key to User.
    """
    def get_object(self, queryset=None, castable=True):
        obj = super(UserDataObjectMixin, self).get_object(queryset)

        if obj.get_class_name() == 'account':
            if obj.id != self.request.user.id:
                raise PermissionDenied

        elif obj.user_id != self.request.user.id:
            raise PermissionDenied

        return obj


class FileResponseMixin(object):
    """Renders a downloadable file format in response to a request.

    Supported file formats are those supported by tablib.

    Current implementation tested on and supported export of Budget \
    and Actual data, where the Actual or Budget is passed in the \
    context as 'object'.

    context['object']

    """
    def render_to_response(self, context):
        "Returns the context renders to the request file format"
        return self.get_file_response(
            self.context_to_file(context)
        )

    def get_file_response(self, export_file, **httpresponse_kwargs):
        dt = datetime.datetime.now().isoformat()
        what = self.kwargs['model']
        response = http.HttpResponse(
            content_type=self._get_content_type(self.kwargs['format'])
        )
        response['Content-Disposition'] = 'attachment; filename=dataset_export_{what}_{dt}.'.format(
                dt=dt,
                what=what
            ) + self.kwargs['format']
        response.write(export_file)
        return response

    def context_to_file(self, context):
        dataset = tablib.Dataset()
        dataset.headers = [
            'CODE',
            'NAME',
            'BUDGET',
            'ACTUAL',
            'DIRECTION'
        ]
        for item in context['object_list']:
            dataset.append(
                [
                    item.node.code,
                    item.node.name,
                    item.budget,
                    item.actual,
                    item.node.direction
                ]
            )
        value = getattr(dataset, self.kwargs['format'])
        return value

    def _get_content_type(self, format):
        if format == 'csv' or format == 'tsv':
            value = 'text/' + format
        elif format == 'json' or format == 'yaml':
            value = 'application/' + format
        elif format == 'xls':
            value = 'application/vnd.ms-excel'
        elif format == 'xlsx':
            value = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return value


class JSONResponseMixin(object):
    """A mixin for optional JSON responses in class-based views."""

    def render_to_json_response(self, context, **response_kwargs):

        data = json.dumps(context)

        response_kwargs['content_type'] = 'application/json'

        return http.HttpResponse(data, **response_kwargs)
