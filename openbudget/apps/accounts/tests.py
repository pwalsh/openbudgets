import random
from django.core.urlresolvers import reverse
from openbudget.apps.accounts.factories import AccountFactory
from openbudget.commons import tests


class UserUITestCase(tests.OpenBudgetsUITestCase):

    """Test account objects over the UI"""

    #listview_name = ''
    detailview_name = 'account_detail'

    def setUp(self):
        self.object = AccountFactory.create()
        self.users = AccountFactory.create_batch(5)

    def test_detailview(self):
        self.client.login(email=self.object.email, password='letmein')
        return UserUITestCase.detailview(self, lookup=self.object.uuid)

    def test_detail_object(self):
        self.client.login(email=self.object.email, password='letmein')
        view = reverse('account_detail', args=(self.object.uuid,))
        response = self.client.get(view)
        self.assertContains(response, self.object.email)

    def test_update_object(self):
        self.client.login(email=self.object.email, password='letmein')
        view = reverse('account_update', args=(self.object.uuid,))
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.object.email)

    def test_object_write_valid(self):
        self.client.login(email=self.object.email, password='letmein')
        view = reverse('account_update', args=(self.object.uuid,))
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.object.email)
        valid_data = {'email': self.object.email, 'first_name': self.object.first_name,
                      'last_name': self.object.last_name, 'language': self.object.language}
        valid_data_response = self.client.post(view, valid_data)
        self.assertEqual(valid_data_response.status_code, 302)

    def test_object_write_invalid(self):
        self.client.login(email=self.object.email, password='letmein')
        view = reverse('account_update', args=(self.object.uuid,))
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.object.email)
        invalid_data = {'email': 'invalid_email_address', 'first_name': self.object.first_name,
                      'last_name': self.object.last_name, 'language': self.object.language}
        invalid_data_response = self.client.post(view, invalid_data)
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


# We don't currently support accounts over the web API
#class UserAPITestCase(tests.OpenBudgetsAPITestCase):
#    """Test account objects over the API"""
#
#    #listview_name = ''
#    detailview_name = 'account_detail'
#
#    def setUp(self):
#       self.object = AccountFactory.create()
#
#    def test_detailview(self):
#        self.client.login(email=self.object.email, password='letmein')
#        return UserUITestCase.detailview(self, lookup=self.object.uuid)
