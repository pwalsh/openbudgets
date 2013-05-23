from datetime import datetime
import tablib
from django.core.mail import send_mail
from openbudget.settings.base import TEMP_FILES_DIR, ADMINS, EMAIL_HOST_USER
from openbudget.apps.transport.incoming.importers import BaseImporter


class TablibImporter(BaseImporter):

    def get_data(self, stream):
        try:
            raw_dataset = tablib.import_set(stream)
        except AttributeError as e:
            # TODO: need to get more specific exception
            self._import_error()
            raise e

        # `_normalize_headers` may transform the headers and returns the same data object
        # we then return the dict view of the data
        return self._normalize_headers(raw_dataset).dict

    def _normalize_headers(self, dataset):
        """Clean the headers of the dataset.

        We replace the existing headers with new ones that \
        have been cleaned and normalized.

        To clean, we strip white space and common joining \
        symbols, and we convert all to lowercase.

        To normalize, we match the header to strings in a \
        string scope map, and convert to the string in the \
        map when our key is either the string or in the scope \
        list.

        """
        #TODO: see if this method can be moved to the BaseImporter in a more generic way
        symbols = {
            ord('_'): None,
            ord('-'): None,
            ord('"'): None,
            ord(' '): None,
            ord("'"): None,
        }
        scopes_map = self._get_header_scopes()

        for index, header in enumerate(dataset.headers):

            tmp = unicode(header).translate(symbols).lower()

            for k, v in scopes_map.iteritems():

                if tmp == k or tmp in v:
                    dataset.headers[index] = k

        return dataset

    def _import_error(self):
        """
        Handle import exception raised by calling `tablib.import_set`
        """

        dt = datetime.now().isoformat()

        this_file = TEMP_FILES_DIR + \
            '/failed_import_{timestamp}_{filename}'.format(
                timestamp=dt,
                filename=unicode(self.sourcefile)
            )

        with open(this_file, 'wb+') as tmp_file:
            for chunk in self.sourcefile.chunks():
                tmp_file.write(chunk)

        # email ourselves that we have a file to check
        subject = 'Open Budget: Failed File Import'
        message = 'The file is attached.'
        sender = EMAIL_HOST_USER
        recipients = [ADMINS]

        send_mail(subject, message, sender, recipients)
