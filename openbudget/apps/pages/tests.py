# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from openbudget.apps.pages.factories import PageFactory


class PageTestCase(TestCase):
    """Tests for pages.Page objects and their related views. urls, etc."""

    def setUp(self):
        self.page = PageFactory.create()

    def test_page_detailview(self):

        detailview = reverse('page',
                args=(self.page.slug,)
            )

        response = self.client.get(detailview)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('page' in response.context)

    def test_404_page(self):
        """Does the 404 page work?"""
        response = self.client.get('/this-page-can-not-possibly-exist-here/')
        self.assertEqual(response.status_code, 404)
