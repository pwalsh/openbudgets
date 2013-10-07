from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class OpenBudgetsUITestCase(TestCase):

    def listview(self):
        """Simple test to verify the UI list view returns what we'd minimally expect"""

        listview = reverse(self.listview_name)
        response = self.client.get(listview)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('object_list' in response.context)

    def detailview(self, lookup=None):
        """Simple test to verify the UI detail view returns what we'd minimally expect"""

        if not lookup:
            lookup = self.object.pk
        detailview = reverse(self.detailview_name,
                             args=(lookup,))
        response = self.client.get(detailview)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('object' in response.context)


class OpenBudgetsAPITestCase(APITestCase):

    def listview(self):
        """Simple test to verify the API list view returns what we'd minimally expect"""
        listview = reverse(self.listview_name)
        response = self.client.get(listview)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def detailview(self):
        """Simple test to verify the API detail view returns what we'd minimally expect"""

        detailview = reverse(self.detailview_name, args=(self.object.pk,))
        response = self.client.get(detailview)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(unicode(self.object.pk), response.data['id'])
