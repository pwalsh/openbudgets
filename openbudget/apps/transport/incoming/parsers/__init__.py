from copy import deepcopy
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from openbudget.apps.budgets.models import PATH_SEPARATOR
from openbudget.apps.transport.incoming.errors import DataValidationError


class BaseParser(object):

    ROUTE_SEPARATOR = PATH_SEPARATOR
    ITEM_SEPARATOR = ';'

    def __init__(self, container_object_dict):
        self.valid = True
        self.dry = False
        self.errors = []
        self.saved_cache = {}
        self.objects_lookup = {}
        self.container_object_dict = container_object_dict

    @classmethod
    def resolve(cls, deferred):
        container_dict = deferred['container']

        if not container_dict:
            raise Exception('Deferred object missing container dict: %s' % container_dict)

        instance = cls(container_dict)
        instance.objects_lookup = deferred['items']

        return instance

    def validate(self, data, keep_cache=False):
        self._generate_lookup(data)

        self.keep_cache = keep_cache
        self.save(dry=True)

        return self.valid, self.errors

    def save(self, dry=False):

        self.dry = dry

        self._create_container()

        if dry:
            # save an untempered copy
            lookup_table_copy = deepcopy(self.objects_lookup)

        for key, obj in self.objects_lookup.iteritems():
            self._save_item(obj, key)

        if dry:
            if not self.keep_cache:
                self._clear_cache()
            # clear all changes by replacing the lookup with the old copy
            self.objects_lookup = lookup_table_copy

        self.dry = False

        return True

    def deferred(self):
        return {
            'container': self.container_object_dict,
            'items': self.objects_lookup
        }

    def throw(self, error):
        self.valid = False
        self.errors.append(error)
        return self

    def _generate_lookup(self, data):
        raise NotImplementedError

    def _save_item(self, obj, key):
        raise NotImplementedError

    def _clean_object(self, obj, key):
        for attr in obj:
            if attr not in self.ITEM_ATTRIBUTES:
                del obj[attr]

    def _create_container(self, container_dict=None, exclude=None):

        data = container_dict or self.container_object_dict

        if not self.dry:
            container = self.container_model.objects.create(**data)
        else:
            container = self.container_model(**data)
            self._dry_clean(container, exclude=exclude)

        self.container_object = container

    def _dry_clean(self, instance, row_num=None, exclude=None):
        try:
            instance.full_clean(exclude=exclude)
        except ValidationError as e:
            self.throw(
                DataValidationError(reasons=e.message_dict, row=row_num)
            )

    def _clear_cache(self):
        self.saved_cache.clear()


PARSERS_MAP = {}


def register(key, parser_class):
    PARSERS_MAP[key] = parser_class


def get_parser(key):
    if key in PARSERS_MAP:
        return PARSERS_MAP[key]
    else:
        raise Exception(_('Parser for key: "%s" does not exist') % key)


def get_parser_key(cls):
    for key, parser_class in PARSERS_MAP.iteritems():
        if cls is parser_class:
            return key
    else:
        raise Exception(_('Given parser is not registered: %s' % unicode(cls)))


def autodiscover():
    # we just load all the other parser modules
    from openbudget.apps.transport.incoming.parsers import budgettemplate, budget, actual


autodiscover()
