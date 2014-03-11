from django.test import TestCase
from django.core.urlresolvers import reverse
from openbudgets.apps.accounts.factories import Account
from openbudgets.apps.entities.factories import Entity
from openbudgets.apps.contexts.factories import Context
from openbudgets.apps.sheets.factories import Sheet


class InteractionTestCase(TestCase):
    """etc."""

    def setUp(self):
        self.users = Account.create_batch(2)
        self.follow_template = 'interactions/partials/_follow.html'
        self.star_template = 'interactions/partials/_star.html'
        self.follow_string = 'form class="interaction follow"'
        self.star_string = 'form class="interaction star"'
        self.entity = Entity.create()
        self.entity_context = Context.create(entity=self.entity)
        self.sheet = Sheet.create(entity=self.entity)
        self.entityview = reverse('entity_detail', args=(self.entity.slug,))
        self.sheetview = reverse('sheet_detail', args=(self.sheet.entity.slug,
                                                       self.sheet.period))

    def test_auth_user_can_star_or_follow(self):
        """If user is auth'd, forms for star/follow are present"""

        self.client.login(email=self.users[0].email, password='letmein')

        response = self.client.get(self.entityview)

        self.assertEqual(response.status_code, 200)
        # TODO: Work out how we can test for "template used", when
        # the template is loaded via a template tag
        #self.assertTemplateUsed(budgetresponse, self.follow_template)
        #self.assertTemplateUsed(budgetresponse, self.star_template)
        #self.assertContains(response, self.follow_string)
        #self.assertContains(response, self.star_string)

        response = self.client.get(self.sheetview)

        self.assertEqual(response.status_code, 200)
        # TODO: Work out how we can test for "template used", when
        # the template is loaded via a template tag
        #self.assertTemplateUsed(budgetresponse, self.follow_template)
        #self.assertTemplateUsed(budgetresponse, self.star_template)
        #self.assertContains(response, self.follow_string)
        #self.assertContains(response, self.star_string)

    def test_anon_user_cant_star_or_follow(self):
        """If user is not auth'd, then the forms don't appear."""

        response = self.client.get(self.entityview)
        self.assertEqual(response.status_code, 200)
        # TODO: Work out how we can test for "template used", when
        # the template is loaded via a template tag
        #self.assertTemplateNotUsed(budgetresponse, self.follow_template)
        #self.assertTemplateNotUsed(budgetresponse, self.star_template)
        #self.assertNotContains(response, self.follow_string)
        #self.assertNotContains(response, self.star_string)

        response = self.client.get(self.sheetview)
        self.assertEqual(response.status_code, 200)
        # TODO: Work out how we can test for "template used", when
        # the template is loaded via a template tag
        #self.assertTemplateNotUsed(budgetresponse, self.follow_template)
        #self.assertTemplateNotUsed(budgetresponse, self.star_template)
        #self.assertNotContains(response, self.follow_string)
        #self.assertNotContains(response, self.star_string)
