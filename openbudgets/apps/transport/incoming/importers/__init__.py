import os
import logging
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from openbudgets.apps.entities.models import Entity
from openbudgets.apps.transport.models import String
from openbudgets.apps.transport.incoming.parsers import get_parser, get_parser_key


class BaseImporter(object):
    """Gets data out of files and into Python data types for further processing.

    This class is abstract and does not implement the required `get_data`
    method. It is provided to make it easy to write alternative importers.

    The default importer for Open Budgets is tablibimporter.TablibImporter,
    which subclasses BaseImporter, and implemented `get_data` using the
    excellent tablib module.

    BaseImporter currently supports import of:

    * Templates (ie: templates and their nodes)
    * Sheets (ie: sheets and their items)

    """

    def __init__(self, sourcefile=None, post_data=None, meta_from_filename=False,
                 ignore_unknown_headers=True, ignore_invalid_rows=False):

        self.sourcefile = sourcefile
        self.post_data = post_data
        self.ignore_unknown_headers = ignore_unknown_headers
        self.ignore_invalid_rows = ignore_invalid_rows
        self.meta_from_filename = meta_from_filename

        if sourcefile:
            self.extract()

    def extract(self):
        """Create a valid dataset from data in the sourcefile.

        We create a dataset object.

        We clean up the headers.

        We email ourselves if the source file cannot be converted \
        to a datset, and we save that sourcefile in a temporary \
        location, as well as emailing it, for analysis.

        """

        logging.info('Executing BaseImporter.extract')

        self._extract_meta()

        data_stream = self.sourcefile.read()
        self.data = self.get_data(data_stream)

        return self

    def validate(self):
        """
        Runs validation on the extracted data using the parser's
        validation.
        """

        logging.info('Executing BaseImporter.validate')

        return self.parser.validate(self.data)

    def save(self):
        """
        Delegates to the parser's save method.
        """

        logging.info('Executing BaseImporter.save')

        return self.parser.save()

    def deferred(self):
        """
        Gets a deferred object from the parser, adding to it
        the parser's class key.

        Returns the deferred object which can be later serialized
        and sent to queue, for later resolving it.
        """

        logging.info('Executing BaseImporter.deferred')

        deferred = self.parser.deferred()
        deferred['class'] = get_parser_key(self.parser.__class__)

        return deferred

    def resolve(self, deferred):
        """
        Takes a deferred importer object which sets the appropriate
        parser and delegates to it's resolve method.
        """

        logging.info('Executing BaseImporter.resolve')

        # get the parser class key
        klass = deferred['class']

        if not klass:
            raise Exception('Deferred object missing class key: %s' % klass)

        # get the parser class and resolve the deferred object
        self.parser = get_parser(klass).resolve(deferred)
        # return self for fluency's sake
        return self

    def get_data(self, stream):
        """
        Takes a data stream read from the source file, extracts a
        dataset from it and stores it in `self.data`.
        """

        logging.info('Executing BaseImporter.get_data')

        raise NotImplementedError()

    def normalize_headers(self, headers):
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

        logging.info('Executing BaseImporter.normalize_headers')

        symbols = {
            # we are now allowing the "_" symbol for translation fields
            # and cases of valid field names such as "map_url"
            # ord('_'): None,
            ord('-'): None,
            ord('"'): None,
            ord(' '): None,
            ord("'"): None,
        }
        scopes_map = self._get_header_scopes()
        normalized_headers = list(headers)

        for index, header in enumerate(headers):

            tmp = unicode(header).translate(symbols).lower()

            for k, v in scopes_map.iteritems():

                if tmp == k or tmp in v:
                    normalized_headers[index] = k

        # MAKE SURE HEADERS ARE LOWER CASED, ALWAYS!
        return [h.lower() for h in normalized_headers]

    def import_error(self):
        """If a file is not validly formed, we can't open it.

        In this case, we send a copy of the file by email to the site admins.

        We want to site admins to be able to see the file, and understand what \
        was invalid - perhaps it is a problem that can be solved in code - \
        file import is part science, part art.
        """

        logging.info('Executing BaseImporter.import_error')

        dt = datetime.now().isoformat()

        attachment = settings.OPENBUDGETS_TEMP_DIR + \
            u'/failed_import_{timestamp}_{filename}'.format(
                timestamp=dt,
                filename=unicode(self.sourcefile)
            )

        with open(attachment, 'wb+') as tmp_file:
            for chunk in self.sourcefile.chunks():
                tmp_file.write(chunk)

        subject = u'Open Budget: Failed File Import'
        message = u'The file is attached.'
        sender = settings.EMAIL_HOST_USER
        recipients = [settings.ADMINS]
        mail = EmailMessage(subject, message, sender, recipients)
        mail.attach_file(attachment)
        mail.send()

    def _extract_meta(self):
        """Get's the meta data for the dataset. \
        The meta data determines the parser class to be used for \
        parsing and saving the data, and the data for creating the \
        container object.

        Each file that is imported has rows of data, where each row \
        is, ultimately, some object. The objects contained in the \
        file also need additional data in order to be contextualized \
        in the datastore.

        For example, if the sourcefile is full of entries that are \
        nodes in a template, we still need to know, for example the \
        name of the template, the entity it belongs to, and so on.

        When data is imported via an interactive wizard, this \
        "metadata" can be filled out in a form by the person doing \
        the import.

        Alternatively, the BaseImporter class also supports parsing \
        the filename of the sourcefile to extract the required \
        metadata. For this option, dataset_meta_in_filename must be \
        True. Importing like this is handy during development, \
        but you'll need to know that your dataset is valid in \
        advance, as there will be no interactive wizard to fix data.

        """

        logging.info('Executing BaseImporter._extract_meta')

        if self.meta_from_filename:
            parser = self._get_parser_from_filename()
        else:
            parser = self._get_parser_from_post()

        self.parser = parser

        return self

    def _get_header_scopes(self):
        """
        Gets the available strings and scopes which are used
        for normalizing the headers.
        """

        logging.info('Executing BaseImporter._get_header_scopes')

        scopes_map = {}

        strings = String.objects.filter(parent__isnull=True)

        for string in strings:
            scopes_map[string.string] = [scope.string for scope in string.scope_set.all()]

        return scopes_map

    def _get_parser_from_filename(self):
        """Extract required metadata for a dataset from the filename.

        This is used for non-interactive importing of datasets from files.

        FILENAME FORMAT:

        TYPE;CONTAINER_OBJECT_KWARGS.EXTENSION

        The first positional argument is always the type (Django model name),
        and the type must be supported by a parser.

        A keyword argument-like pattern is used for the attributes of the
        container object.

        Arguments are separated by:

        settings.OPENBUDGETS_IMPORT_FIELD_DELIMITER

        defaults to ','.

        Multiple values for keys are separated by:

        settings.OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER

        defaults to '|'.

        EXAMPLES
        --------

        TEMPLATE:
        template,name=israel-municipality,divisions=4|5|6,period_start=2001-01-10.csv
        Each row in the file is a node in the template.

        SHEET:
        sheet,entity=slug,period_start=2001-01-01,period_end=2001-12-31.csv
        Each row in the file is an item in the budget.

        """

        logging.info('Executing BaseImporter._get_parser_from_filename')

        ARGS_DELIMITER = settings.OPENBUDGETS_IMPORT_FIELD_DELIMITER
        VALS_DELIMITER = settings.OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER

        # an empty dict to populate with data for our container object
        container_object_dict = {}

        # an empty dict to work with while creating the final container dict
        unprocessed_arguments_dict = {}

        # get our data string from the filename
        keys, ext = os.path.splitext(unicode(self.sourcefile))

        # first, split the parser key from the container_object keys
        arguments = keys.split(ARGS_DELIMITER)

        # get the appropriate parser class
        parser_key = arguments[0]
        parser = get_parser(parser_key)

        for argument in arguments[1:]:

            argument_key, argument_value = argument.split('=')

            if VALS_DELIMITER in argument_value:
                argument_value = tuple(argument_value.split(VALS_DELIMITER))

            # the arguments we got, now as a dictionary
            unprocessed_arguments_dict[argument_key] = argument_value

        # some special conditions, depending on type
        if parser_key == 'sheet':
            unprocessed_arguments_dict['entity'] = Entity.objects.get(
                slug=unprocessed_arguments_dict['entity'])

        # remove non-valid arguments
        for k in unprocessed_arguments_dict.copy():
            if not k in parser.CONTAINER_ATTRIBUTES:
                del unprocessed_arguments_dict[k]

        # update the empty container_object_dict with valid arguments
        container_object_dict.update(unprocessed_arguments_dict)

        # return instantiated parser
        return parser(container_object_dict)

    def _get_parser_from_post(self):
        """Extract required metadata for a dataset from request.POST."""

        logging.info('Executing BaseImporter._get_parser_from_post')

        VALS_DELIMITER = settings.OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER

        container_object_dict = {}
        parser_key = self.post_data.get('type', '')
        attributes = self.post_data
        del attributes['type']

        logging.info('BaseImporter._get_parser_from_post :: parser_key:' + parser_key)

        # get the appropriate parser class
        parser = get_parser(parser_key)

        logging.info('BaseImporter._get_parser_from_post :: parser.container_model:')
        logging.info(parser.container_model())

        logging.info('BaseImporter._get_parser_from_post :: attributes.items:')
        logging.info(attributes.items())

        for k, v in attributes.items():

            logging.info('BaseImporter._get_parser_from_post :: attributes key-value pair:')
            logging.info(k, v)

            try:
                getattr(parser.container_model(), k)
            except AttributeError as e:
                raise e

            # if the value is delimited, it is an m2m related field
            if VALS_DELIMITER in v:
                v = tuple(v.split(VALS_DELIMITER))

            container_object_dict[k] = v

            # return instantiated parser
            return parser(container_object_dict)

        else:
            raise Exception('No attributes given in meta data.')
