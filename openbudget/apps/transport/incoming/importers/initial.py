# -*- coding: UTF-8

"""

This code is current only invoked via a management command. It is pretty
dirty, but works for our needs now. Opened an issue to possibly refactor this
in the future, here: https://github.com/hasadna/omuni-budget/issues/144

"""


import os
import datetime
import tablib
from openbudget.apps.transport.models import String
from openbudget.apps.entities.models import Domain, Division, Entity


class InitImporter(object):
    """."""

    def __init__(self, sourcefile, ignore_unknown_headers=False,
                 ignore_invalid_rows=False, dataset_meta_in_filename=False):

        self.sourcefile = sourcefile
        self.ignore_unknown_headers = ignore_unknown_headers
        self.ignore_invalid_rows = ignore_invalid_rows
        self.dataset_meta_in_filename = dataset_meta_in_filename
        self.models = {
            'domains': Domain,
            'divisions': Division,
            'entities': Entity
        }

    def save(self):
        """."""
        f = open(self.sourcefile, 'r')
        stream = f.read()
        tmp, ext = os.path.basename(self.sourcefile).split('.')
        model = tmp.split('_')[1]

        try:
            raw_dataset = tablib.import_set(stream)
        except AttributeError as e:
            raise e

        dataset = self._normalize_headers(raw_dataset)

        for item in dataset.dict:

            for x in item.keys():
                if item[x] == '':
                    del item[x]

            ## TODO: FIX THIS JUST WORKING AROUND SOME MODELTRANS ISSUE
            item['name_he'] = item['name']
            if 'description' in item:
                item['description_he'] = item['description']

            if model == 'divisions':
                # got keywords, not IDs
                item['domain'] = Domain.objects.get(name_he=item['domain'])

            if model == 'entities':
                # got keywords, need IDs
                item['division'] = Division.objects.get(name_he=item['division'])
                if 'parent' in item:

                    if item['division'].index != 1:
                        item['parent'] = Entity.objects.get(name_he=item['parent'], division__name_he=u'מחוז')
                    else:
                        item['parent'] = Entity.objects.get(name_he=item['parent'])

            self.models[model].objects.create(**item)

    def _normalize_headers(self, dataset):

        symbols = {
            ord('_'): None,
            ord('-'): None,
            ord('"'): None,
            ord(' '): None,
            ord("'"): None,
        }

        for index, header in enumerate(dataset.headers):
            tmp = unicode(header).lower()
            dataset.headers[index] = tmp
        value = dataset
        return value

    def _get_header_aliases(self):
        value = {}
        strings = String.objects.filter(parent__isnull=True)
        for string in strings:
           value[string.string] = [alias.string for alias in string.scope_set.all()]
        return value
