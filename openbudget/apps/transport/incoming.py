import datetime
import tablib
from openbudget.settings.base import TEMP_FILES_DIR, ADMINS
from openbudget.apps.transport import models


class FileImport(object):
    """Gets data out of files and into the database.


    """
    def __init__(self, sourcefile=None, datatype=None):
        self.source_file = sourcefile
        self.data_type = datatype

    def get_datatype_from_filename(sourcefile):
        """Import data correctly by file naming convention.

        This handy method allows us to import data without an
        interactive wizard.
        """
        pass

    def to_dataset(sourcefile):
        try:
            tablib.import_set(sourcefile)
        except Exception, e: #TODO: Check the possible exceptions

            # save the file for analysis in case of exception
            dt = datetime.datetime.now().isoformat()
            this_file = TEMP_FILES_DIR + '/failed_import_{}.sourcefile'.format(dt)
            with open(this_file, 'wb+') as tmp_file:
                for chunk in fobj.chunks():
                    tmp_file.write(chunk)

            # email ourselves that we have a file to check
            subject = 'Open Budget: Failed File Import'
            message = 'The file is attached.'
            sender = EMAIL_HOST_USER
            recipients = [ADMINS]
            send_mail(subject, message, sender, recipients)

            # tell the customer what happened and what will happen
            return ''

    def persist_sourcefile(sourcefile):
        """Saves an uploaded source file to a work directory."""
        pass

    def create_dataset(sourcefile):
        """Returns a Tablib dataset from a given source file."""
        pass

    def clean_headers(dataset):
        """Clean the headers of the existing dataset.

        To clean, we strip white space and common joining symbols.
        And, we convert everything to lowercase.
        """
        symbols = {
            ord('_'): None,
            ord('-'): None,
            ord('"'): None,
            ord(' '): None,
            ord("'"): None,
        }

        for header in dataset.headers:
            header.translate(symbols).lower()

        value = dataset
        return value

    def get_header_aliases():
        value = []
        header_strings = models.String.objects.filter(parent__isnull=True)
        for string in header_strings:
           value.append(
                (
                    string.string,
                    [alias.string for alias in string.alias_set.all()]
                )
            )
        return value

    def normalize_headers(dataset):
        """Normalize the headers of the existing dataset.

        Headers are normalized according to a defalt set of string
        mappings, and sets of related strings entered via site admins.
        """
        #header_maps = get_header_maps() - want DICT, not list
        for header in dataset.headers:
            try:
                new = header_maps[header]
            except KeyError:
                new = header
            value.append(new)
        return value

    def validate_data_structure(dataset):
        """Validate the data structure against a template"""
        # get template
        # validate headers
        # validate nodes
        # return tuple of (bool, list(co-ordinates))
        # the list will match the bool value, so if it is false
        # a list of false co-ordinates, and if true, a list of true
        # presuming i can use the list of tru in subsequent function
        # need to see if that is so
        pass

    def validate_data_values(dataset):
        """Validate that the data values match the expected input"""
        # check type matches expected
        # return tuple of (bool, list(co-ordinates))
        # the list will match the bool value, so if it is false
        # a list of false co-ordinates, and if true, a list of true
        # presuming i can use the list of tru in subsequent function
        # need to see if that is so
        pass

    def to_db(dataset):
        """Save a dataset to the database"""
        pass
