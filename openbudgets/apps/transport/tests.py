import tempfile
import tablib
from django.test import TestCase
from openbudgets.apps.entities import factories
from openbudgets.apps.transport.incoming.importers.tablibimporter import TablibImporter


class ImporterTestCase(TestCase):

    def setUp(self):

        self.domain = factories.Domain.create()
        self.division = factories.Division.create()
        self.entity = factories.Entity.create()
        self.template_headers = ['code', 'parent', 'parent_scope',
                                 'direction', 'inverse', 'inverse_scope',
                                 'comparable', 'name', 'description']
        self.template_meta = {
            'type': 'template',
            'name': 'Test Template',
            'divisions': self.division.name,
            'period_start': '1994-01-01'}
        self.template_dataset = tablib.Dataset(headers=self.template_headers)
        self.sheet_headers = ['parent', 'parent_scope',
                              'code', 'budget', 'actual',
                              'comparable', 'name', 'description']
        self.sheet_meta = {
            'type': 'sheet',
            'entity': self.entity.slug,
            'period_start': '2000-01-01',
            'period_end': '2001-01-01'}
        self.sheet_dataset = tablib.Dataset(headers=self.sheet_headers)

    #def test_something(self):
    #
    #    importer = TablibImporter(self.template_dataset.csv, self.template_meta, False)
    #    valid, errors = importer.validate()

    def test_csv_to_dataset(self):
        with tempfile.NamedTemporaryFile() as csv_file:
            csv_file.write(','.join(self.template_headers))
            for l in csv_file.readlines():
                    headers_from_file = l[0].split(',')
                    self.assertEqual(self.template_dataset.headers, headers_from_file)

    def test_get_parser_from_filename(self):
        pass

    def test_get_parser_from_post(self):
        pass

