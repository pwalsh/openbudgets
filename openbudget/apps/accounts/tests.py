import random
from django.test import TestCase
from django.core.urlresolvers import reverse
from openbudget.apps.accounts.factories import AccountFactory


class UserTestCase(TestCase):

    """Tests for Account objects and their related views, urls, etc."""

    def setUp(self):
        self.users = AccountFactory.create_batch(5)

    def test_detailview_read(self):

        """Check that a user's account detail view works."""

        for user in self.users:
            self.client.login(email=user.email, password='letmein')
            detailview = reverse('account_detail', args=(user.uuid,))
            response = self.client.get(detailview)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, user.email)

    def test_updateview_read(self):

        """Check that a user's account update view works."""

        for user in self.users:
            self.client.login(email=user.email, password='letmein')
            updateview = reverse('account_update', args=(user.uuid,))
            response = self.client.get(updateview)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, user.email)

    def test_updateview_write(self):

        """Check that a user's account update view can be written to."""

        for user in self.users:
            self.client.login(email=user.email, password='letmein')
            updateview = reverse('account_update', args=(user.uuid,))
            response = self.client.get(updateview)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, user.email)

            valid_data = {'email': user.email, 'first_name': user.first_name,
                          'last_name': user.last_name, 'language': user.language}
            invalid_data = valid_data.copy()
            invalid_data['email'] = 'invalid_email_address'
            valid_data_response = self.client.post(updateview, valid_data)
            invalid_data_response = self.client.post(updateview, invalid_data)

            self.assertEqual(valid_data_response.status_code, 302)
            self.assertEqual(invalid_data_response.status_code, 200)

    def test_detailview_read_for_anonymous_user(self):

        """Ensure that an anon user can't reach an account detail view."""

        for user in self.users:
            detailview = reverse('account_detail', args=(user.uuid,))
            response = self.client.get(detailview)

            self.assertEqual(response.status_code, 302)

    def test_updateview_read_for_anonymous_user(self):

        """Ensure that an anon user can't reach an account update view."""

        for user in self.users:
            updateview = reverse('account_update', args=(user.uuid,))

            response = self.client.get(updateview)

            self.assertEqual(response.status_code, 302)

    def test_detailview_read_for_wrong_user(self):

        """Ensure that a user can't read another user's detail view."""

        for user in self.users:
            detailview = reverse('account_detail', args=(user.uuid,))

            other_users = self.users
            other_users.remove(user)
            random_user = random.choice(self.users)

            self.client.login(email=random_user.email, password='letmein')

            response = self.client.get(detailview)

            self.assertEqual(response.status_code, 403)

    def test_updateview_read_for_wrong_user(self):

        """Ensure that an auth user can't read another user's update view."""

        for user in self.users:
            updateview = reverse('account_update', args=(user.uuid,))
            other_users = self.users
            other_users.remove(user)
            random_user = random.choice(other_users)

            self.client.login(email=random_user.email, password='letmein')

            response = self.client.get(updateview)

            self.assertEqual(response.status_code, 403)

    def test_updateview_write_for_anonymous_user(self):

        """Ensure that an anon user can't write to user's update view."""

        for user in self.users:
            updateview = reverse('account_update', args=(user.uuid,))
            valid_data = {'email': user.email, 'first_name': user.first_name,
                          'last_name': user.last_name, 'language': user.language}
            invalid_data = valid_data.copy()
            invalid_data['email'] = 'invalid_email_address'
            valid_data_response = self.client.post(updateview, valid_data)
            invalid_data_response = self.client.post(updateview, invalid_data)

            self.assertEqual(valid_data_response.status_code, 302)
            self.assertEqual(invalid_data_response.status_code, 302)

    def test_updateview_write_for_wrong_user(self):

        """Ensure that an auth user can't write to another user's update view."""

        for user in self.users:
            updateview = reverse('account_update', args=(user.uuid,))
            other_users = self.users
            other_users.remove(user)
            random_user = random.choice(other_users)

            self.client.login(email=random_user.email, password='letmein')

            valid_data = {'email': user.email, 'first_name': user.first_name,
                          'last_name': user.last_name, 'language': user.language}
            invalid_data = valid_data.copy()
            invalid_data['email'] = 'invalid_email_address'
            valid_data_response = self.client.post(updateview, valid_data)
            invalid_data_response = self.client.post(updateview, invalid_data)

            self.assertEqual(valid_data_response.status_code, 403)
            self.assertEqual(invalid_data_response.status_code, 403)
