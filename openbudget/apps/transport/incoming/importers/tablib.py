import tablib
from openbudget.apps.transport.incoming.importers import BaseImporter


class TablibImporter(BaseImporter):
    """
    Implements the BaseImporter using Tablib for extracting data our of the
    file's data stream.
    """

    def get_data(self, stream):
        try:
            raw_dataset = tablib.import_set(stream)
        except AttributeError as e:
            # TODO: need to get more specific exception
            self.import_error()
            raise e

        # `_normalize_headers` may transform the headers and returns the same data object
        raw_dataset.headers = self._normalize_headers(raw_dataset.headers)

        # we then return the dict view of the data
        return raw_dataset.dict
