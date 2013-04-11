import random
from django.test import TestCase
from django.core.urlresolvers import reverse
from openbudget.apps.accounts.factories import UserFactory, UserProfileFactory


class UserTestCase(TestCase):
    """Tests for User objects and their related views, urls, etc."""

    def setUp(self):
        self.users = UserFactory.create_batch(5)

    def test_detailview_read(self):
        for user in self.users:
            login = self.client.login(
                username=user.username,
                password='letmein'
            )
            detailview = reverse(
                'account_detail',
                args=(user.get_profile().uuid,)
            )
            response = self.client.get(detailview)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, user.email)

    def test_updateview_read(self):
        for user in self.users:
            login = self.client.login(
                username=user.username,
                password='letmein'
            )
            updateview = reverse(
                'account_update',
                args=(user.get_profile().uuid,)
            )
            response = self.client.get(updateview)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, user.email)

    def test_updateview_write(self):
        for user in self.users:
            login = self.client.login(
                username=user.username,
                password='letmein'
            )
            updateview = reverse(
                'account_update',
                args=(user.get_profile().uuid,)
            )
            response = self.client.get(updateview)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, user.email)
            valid_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'language': user.get_profile().language
            }
            invalid_data = valid_data.copy()
            invalid_data['email'] = 'invalid_email_address'
            valid_data_response = self.client.post(
                updateview,
                valid_data
            )
            invalid_data_response = self.client.post(
                updateview,
                invalid_data
            )
            self.assertEqual(valid_data_response.status_code, 302)
            self.assertEqual(invalid_data_response.status_code, 200)

    def test_detailview_read_for_anonymous_user(self):
        for user in self.users:
            detailview = reverse(
                'account_detail',
                args=(user.get_profile().uuid,)
            )
            response = self.client.get(detailview)
            self.assertEqual(response.status_code, 302)

    def test_updateview_read_for_anonymous_user(self):
        for user in self.users:
            updateview = reverse(
                'account_update',
                args=(user.get_profile().uuid,)
            )
            response = self.client.get(updateview)
            self.assertEqual(response.status_code, 302)

    def test_detailview_read_for_wrong_user(self):
        for user in self.users:
            detailview = reverse(
                'account_detail',
                args=(user.get_profile().uuid,)
            )
            other_users = self.users
            other_users.remove(user)
            random_user = random.choice(self.users)
            login = self.client.login(
                username=random_user.username,
                password='letmein'
            )
            response = self.client.get(detailview)
            self.assertEqual(response.status_code, 403)

    def test_updateview_read_for_wrong_user(self):
        for user in self.users:
            updateview = reverse(
                'account_update',
                args=(user.get_profile().uuid,)
            )
            other_users = self.users
            other_users.remove(user)
            random_user = random.choice(other_users)
            login = self.client.login(
                username=random_user.username,
                password='letmein'
            )
            response = self.client.get(updateview)
            self.assertEqual(response.status_code, 403)

    def test_updateview_write_for_anonymous_user(self):
        for user in self.users:
            updateview = reverse(
                'account_update',
                args=(user.get_profile().uuid,)
            )
            valid_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'language': user.get_profile().language
            }
            invalid_data = valid_data.copy()
            invalid_data['email'] = 'invalid_email_address'
            valid_data_response = self.client.post(
                updateview,
                valid_data
            )
            invalid_data_response = self.client.post(
                updateview,
                invalid_data
            )
            self.assertEqual(valid_data_response.status_code, 302)
            self.assertEqual(invalid_data_response.status_code, 302)

    def test_updateview_write_for_wrong_user(self):
        for user in self.users:
            updateview = reverse(
                'account_update',
                args=(user.get_profile().uuid,)
            )
            other_users = self.users
            other_users.remove(user)
            random_user = random.choice(other_users)
            login = self.client.login(
                username=random_user.username,
                password='letmein'
            )
            valid_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'language': user.get_profile().language
            }
            invalid_data = valid_data.copy()
            invalid_data['email'] = 'invalid_email_address'
            valid_data_response = self.client.post(
                updateview,
                valid_data
            )
            invalid_data_response = self.client.post(
                updateview,
                invalid_data
            )
            self.assertEqual(valid_data_response.status_code, 403)
            self.assertEqual(invalid_data_response.status_code, 403)
