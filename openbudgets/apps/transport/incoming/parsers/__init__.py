from copy import deepcopy
from string import replace
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from openbudgets.apps.transport.incoming.errors import DataValidationError


ITEM_SEPARATOR = settings.OPENBUDGETS_IMPORT_INTRA_FIELD_MULTIPLE_VALUE_DELIMITER


class ParsingError(Exception):
    pass


class BaseParser(object):
    """
    Parsers take a raw dataset, usually from an importer, and transform
    it ultimately to persisted data in the datastore.

    This process is combined from 2 steps: validate and save.

    If the two steps are to be divided asynchronously then it's possible to
    get a serializable deferred object after validation, which can later be
    resolved and saved by the same parser class.
    """

    #PATH_DELIMITER = settings.OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER
    PATH_DELIMITER = ','
    ITEM_SEPARATOR = ITEM_SEPARATOR
    ITEM_CLEANING_EXCLUDE = tuple()

    def __init__(self, container_object_dict):
        self.valid = True
        self.dry = False
        self.errors = []
        self.saved_cache = {}
        self.objects_lookup = {}
        # we usually get this from the importer
        self.container_object_dict = container_object_dict
        # objects to delete at the end of process
        self.dirty_list = []

    @classmethod
    def resolve(cls, deferred):
        """
        Resolve a deferred representation of a parser's data.
        Instantiates the class and returns an instance that
        should be ready for saving.
        """
        container_dict = deferred['container']

        if not container_dict:
            raise Exception('Deferred object missing container dict: %s' % container_dict)

        instance = cls(container_dict)
        instance.objects_lookup = deferred['items']

        # basically we're only sure the objects lookup is generated but this
        # should have been side effect of validating the data
        return instance

    def clean(self, data):
        for row_num, obj in enumerate(data):
            parent_scope = obj.get('parentscope')
            inverse_scopes = obj.get('inversescope')

            if parent_scope:
                obj['parentscope'] = replace(parent_scope, '|', ',')

            if inverse_scopes:
                inverse_scopes = [replace(scope, '|', ',') for scope in ITEM_SEPARATOR.split(inverse_scopes)]
                obj['inversescope'] = ITEM_SEPARATOR.join(inverse_scopes)

        return data

    def validate(self, data, keep_cache=False):
        """
        Takes a dataset, cleans it, prepares it for saving
        and runs all possible validations to make sure
        that a consecutive call on this prepared data
        sends it straight to the datastore without any exceptions.

        It generate a lookup dictionary of the dataset that will later be
        iterated upon when saving.

        If the `keep_cache` argument is `True` then the parser's `saved_cache`
        property, used for storing item instances created from the dataset, is
        not cleared at the end of the validation.
        You'll have to explicitly call `_clear_cache()` after that when you
        need to.

        Returns a boolean if validation is successful and a list of errors that
        were thrown during validation.
        """
        data = self.clean(data)

        # generate a lookup table with each item uniquely identified
        self._generate_lookup(data)

        self.keep_cache = keep_cache
        # run a dry save of the data
        self.save(dry=True)

        return self.valid, self.errors

    def save(self, dry=False):
        """
        Saves the pre-stored objects in the `objects_lookup` dict, as items.
        Also creates the container from the data given on instantiation.

        When running in dry mode nothing is actually saved to the datastore
        and nothing is persisted.
        All the generated model instances are stored in the `saved_cache` dict
        and never saved to datastore.
        """
        self.dry = dry

        # create an instance of the container
        self._create_container()

        if dry:
            # save an untempered copy
            lookup_table_copy = deepcopy(self.objects_lookup)

        # loop the lookup table and save every item
        self._save_items()

        if dry:
            if not self.keep_cache:
                self._clear_cache()
            # clear all changes by replacing the lookup with the old copy
            self.objects_lookup = lookup_table_copy

        self.dry = False

        return True

    def deferred(self):
        """
        Generates and returns a deferredable representation of the
        parser.
        """
        return {
            'container': self.container_object_dict,
            'items': self.objects_lookup
        }

    def throw(self, error):
        """
        Takes an error instance from the `incoming.errors` module and
        appends it to the list of errors.
        Also makes sure `valid` is `False`.
        """
        self.valid = False
        self.errors.append(error)
        return self

    def cleanup(self, *objects):

        """Delete all unneeded entities."""

        if len(objects):
            # if used as a setter, append objects to the list
            self.dirty_list += objects

        else:
            # used as getter simply flush the list
            for item in self.dirty_list:
                item.delete()

        return self

    def _generate_lookup(self, data):
        """
        Generates the data's objects lookup table for saving them later.

        This method needs to be implemented by non-abstract implementations.
        """
        raise NotImplementedError

    def _save_items(self):
        """Saves all the objects in `self.objects_lookup` into DB.

        If this is a dry run then just attempts to validate the save process.
        """
        for key, obj in self.objects_lookup.iteritems():
            self._save_item(obj, key)

    def _save_item(self, obj, key):
        """
        Saves a given object as an item - as in instance of `item_model` attribute.

        This method needs to be implemented by non-abstract implementations.
        """
        raise NotImplementedError

    def _create_item(self, obj, key):
        self._clean_object(obj, key)

        if not self.dry:
            item = self.item_model.objects.create(**obj)
        else:
            item = self.item_model(**obj)
            row_num = self.rows_objects_lookup.get(key, None)
            self._dry_clean(item, row_num=row_num, exclude=self.ITEM_CLEANING_EXCLUDE)

        return item

    def _clean_object(self, obj, key):
        """
        Cleans an object before it's used as attributes for an item's
        model instance creation.
        Removes every attribute that is not in the `ITEM_ATTRIBUTES` dict.
        """
        attrs_to_clean = []
        for attr in obj:
            if attr not in self.ITEM_ATTRIBUTES:
                attrs_to_clean.append(attr)
        if len(attrs_to_clean):
            for attr in attrs_to_clean:
                del obj[attr]

    def _create_container(self, container_dict=None, exclude=None):
        """
        Creates a model instance of the `container_model`.
        """
        data = container_dict or self.container_object_dict

        if not self.dry:
            container = self.container_model.objects.create(**data)
        else:
            container = self.container_model(**data)
            self._dry_clean(container, exclude=exclude)

        self.container_object = container

    def _dry_clean(self, instance, row_num=None, exclude=None):
        """
        Calls a given `instance`'s `full_clean()` method for validating it.
        Validation errors are caught and exchanged for errors thrown to the
        parser using `throw()`.
        """
        try:
            instance.full_clean(exclude=exclude)
        except ValidationError as e:
            self.throw(DataValidationError(reasons=e.message_dict, row=row_num))

    def _clear_cache(self):
        """
        Clears the `saved_cache` dict.
        """
        self.saved_cache.clear()


PARSERS_MAP = {}


def register(key, parser_class):
    """
    Registers a parser class in the system.
    """
    PARSERS_MAP[key] = parser_class


def get_parser(key):
    """
    Gets a parser class from the registry using a string key.
    """
    if key in PARSERS_MAP:
        return PARSERS_MAP[key]
    else:
        raise Exception(_('Parser for key: "{key}" does not exist').format(key=key))


def get_parser_key(cls):
    """
    Gets the key from the registry under which this parser class
    is stored, mostly for deferring that parser for later use.
    """
    for key, parser_class in PARSERS_MAP.iteritems():
        if cls is parser_class:
            return key
    else:
        raise Exception(_('Given parser is not registered: {klass}'.format(
            klass=unicode(cls))))


def autodiscover():
    # we just load all the other parser modules
    from openbudgets.apps.transport.incoming.parsers import template, sheet


autodiscover()
