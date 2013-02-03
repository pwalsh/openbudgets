# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class UserTestCase(TestCase):
    """Tests for User objects and their related views, urls, etc."""

    fixtures = ['test_accounts.json']

    def test_user_profile(self):
        user = User.objects.get(pk=1)
        profile_url = reverse('user_profile_detail', args=(user.get_profile().uuid,))
        self.client.login(username=user.username, password='morelove!')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.email)

    def test_user_profile_is_private(self):
        user = User.objects.get(pk=1)
        profile_url = reverse('user_profile_detail', args=(user.get_profile().uuid,))
        response = self.client.get(profile_url)
        # User is anonymous, redirect to login screen
        self.assertEqual(response.status_code, 302)
