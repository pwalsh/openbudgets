# -*- coding: UTF-8

"""

This code is current only invoked via a management command. It is pretty
dirty, but works for our needs now. Opened an issue to refactor this
in the future, here: https://github.com/hasadna/omuni-budget/issues/144

"""


import os
import datetime
import tablib
from openbudgets.apps.transport.models import String
from openbudgets.apps.entities.models import Domain, Division, Entity


class CSVImporter(object):

    def __init__(self, model, sourcefile):

        self.sourcefile = sourcefile
        self.models = {
            'domains': Domain,
            'divisions': Division,
            'entities': Entity,
        }
        self.model = self.models[model]
        self.raw_dataset = self.extract()
        self.data = self.clean(self.raw_dataset)
        self.save()

    def extract(self):
        """Create a tablib Dataset object from the sourcefile."""
        stream = self.sourcefile.read()
        raw_dataset = tablib.import_set(stream)
        return raw_dataset

    def clean(self, raw_dataset):
        """File-level cleanup."""
        dataset = self._normalize_headers(raw_dataset)
        return dataset

    def _normalize_headers(self, dataset):

        symbols = {
            # Note: We are now allowing the "_" symbol which is valid in python vars.
            ord('-'): None,
            ord('"'): None,
            ord(' '): None,
            ord("'"): None,
            }

        for index, header in enumerate(dataset.headers):
            tmp = unicode(header).translate(symbols).lower()
            dataset.headers[index] = tmp

        return dataset

    def save(self):

        for item in self.data.dict:
            for k, v in item.iteritems():

                if item[k] == '':
                    del item[k]

                #hmmmm
                if 'id' in item:
                    del item['id']

            m2ms = []

            #hmmmm
            if self.model == Grade:
                item['region'] = Region.objects.get(name=item['region'])

            elif self.model == Topic:

                if 'parent' in item and item['parent']:
                    item['parent'] = Topic.objects.get(name=item['parent'])

                if 'grades' in item and item['grades']:
                    grades = item['grades'].split(settings.SLATEMATH_IMPORT_FIELD_MULTIPLE_VALUE_DELIMITER)
                    for grade in grades:
                        grade = grade.strip()
                        grade = Grade.objects.get(name=grade)
                        m2ms.append(grade)

                    del item['grades']
                    #del item['codes']


            elif self.model == Episode:

                asset_root = 'http://' + Site.objects.get(pk=1).domain + settings.SLATEMATH_EPISODES_URL \
                             + '/' + item['slug'] + '/' + item['slug'] + '.html'

                item['assets'] = asset_root

                if 'topics' in item and item['topics']:
                    topics = item['topics'].split(settings.SLATEMATH_IMPORT_FIELD_MULTIPLE_VALUE_DELIMITER)
                    for topic in topics:
                        topic = topic.strip()

                        # only temp because topic is not unique enough
                        topic = Topic.objects.filter(name=topic)[0]
                        m2ms.append(topic)

                    del item['topics']

            obj = self.model.objects.create(**item)

            if self.model == Episode:
                image = 'http://' + Site.objects.get(pk=1).domain + settings.SLATEMATH_EPISODES_URL \
                        + '/' + item['slug'] + '/thumbnail.png'
                EpisodeImage.objects.create(episode=obj, image=image, region=Region.objects.all()[0])

            if m2ms and self.model == Topic:
                for o in m2ms:
                    obj.grades.add(o)

            elif m2ms and self.model == Episode:
                for o in m2ms:
                    obj.topics.add(o)


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

            for k, v in item.iteritems():

                if item[k] == '':
                    del item[k]

                if v == 'TRUE':
                    item[k] = True

                if v == 'FALSE':
                    item[k] = False

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
