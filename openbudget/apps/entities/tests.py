import random
from django.test import TestCase
from django.core.urlresolvers import reverse
from openbudget.apps.entities.factories import EntityFactory


class EntityTestCase(TestCase):

    def setUp(self):
        self.entities = EntityFactory.create_batch(5)

    def test_listview(self):

        listview = reverse(
            'entity_list'
        )

        response = self.client.get(listview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)

    #def test_detailview(self):
    #    for entity in self.entities:
    #
    #        detailview = reverse(
    #            'entity_detail',
    #            args=(entity.slug,)
    #        )

    #        response = self.client.get(detailview)

    #        self.assertEqual(response.status_code, 200)
    #        self.assertTrue('object' in response.context)
