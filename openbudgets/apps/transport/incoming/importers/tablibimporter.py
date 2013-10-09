import logging
import tablib
from openbudgets.apps.transport.incoming.importers import BaseImporter


class TablibImporter(BaseImporter):

    """Implemented the `get_data` method using the tablib module to convert the
    file stream to a Python ordered dict.

    """

    def get_data(self, stream):

        logging.info('Executing TablibImporter._get_parser_from_post')

        try:
            raw_dataset = tablib.import_set(stream)

        except AttributeError as e:
            self.import_error()
            raise e

        # `normalize_headers`, and return the updated dataset object.
        raw_dataset.headers = self.normalize_headers(raw_dataset.headers)

        # return the dict view of the data
        return raw_dataset.dict
