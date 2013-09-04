import random
from django.test import TestCase
from django.core.urlresolvers import reverse
from openbudget.apps.entities.factories import EntityFactory


class EntityTestCase(TestCase):

    def setUp(self):
        self.entity = EntityFactory.create()

    def test_listview(self):

        listview = reverse('entity_list')
        response = self.client.get(listview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)

    def test_entity_detailview(self):

        detailview = reverse('entity_detail', args=(self.entity.slug,))
        response = self.client.get(detailview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)
