# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class UserTestCase(TestCase):
    """Tests for User objects and their related views, urls, etc."""

    fixtures = ['test_accounts.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user1_profile_detail = reverse('user_profile_detail', args=(self.user1.get_profile().uuid,))
        self.user1_profile_update = reverse('user_profile_update', args=(self.user1.get_profile().uuid,))

        self.user2 = User.objects.get(pk=2)
        self.user2_profile_detail = reverse('user_profile_detail', args=(self.user2.get_profile().uuid,))
        self.user2_profile_update = reverse('user_profile_update', args=(self.user2.get_profile().uuid,))

    def test_user_profile_detail(self):
        self.client.login(username=self.user1.username, password='morelove!')
        response = self.client.get(self.user1_profile_detail)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.email)

    def test_user_profile_update(self):
        self.client.login(username=self.user1.username, password='morelove!')
        response = self.client.get(self.user1_profile_update)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.email)

    def test_user_profile_views_private(self):
        # Can we reach profile views when not logged in?
        # We expect to be redirected to the login page
        response_detail = self.client.get(self.user1_profile_detail)
        self.assertEqual(response_detail.status_code, 302)
        response_update = self.client.get(self.user1_profile_update)
        self.assertEqual(response_update.status_code, 302)

        # Can we reach the profile views of another user?
        # We expect to get PermissionDenied due to use of our
        # UserDataObjectMixin custom mixin for CBVs.
        self.client.login(username=self.user2.username, password='morelove!')
        response_detail = self.client.get(self.user1_profile_detail)
        self.assertEqual(response_detail.status_code, 403)
        response_update = self.client.get(self.user1_profile_update)
        self.assertEqual(response_update.status_code, 403)
