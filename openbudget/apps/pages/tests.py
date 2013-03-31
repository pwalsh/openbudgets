# -*- coding: utf-8 -*-

from django.test import TestCase


class PageTestCase(TestCase):
    """Tests for pages.Page objects and their related views. urls, etc."""

    fixtures = ['test_pages.json']

    def test_en_page(self):
        """Test pages with English slugs, and check template."""
        response = self.client.get('/test/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page' in response.context)
        self.assertContains(response, 'A test page for English pages.')

    def test_he_page(self):
        """Test pages with Hebrew slugs, and check template."""
        response = self.client.get('/בדיקה/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page' in response.context)
        self.assertContains(response, 'בדיקה לדפיים עבריים.')

    def test_404_page(self):
        """Does the 404 page work?"""
        response = self.client.get('/this-page-can-not-possibly-exist-here/')
        self.assertEqual(response.status_code, 404)
