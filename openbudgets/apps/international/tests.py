import random
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from openbudgets.apps.accounts.factories import Account
from openbudgets.commons.factories import SiteFactory
from openbudgets.apps.international.utilities import get_language_key


class InternationalCase(TestCase):
    """Tests for custom language functionality."""

    def setUp(self):
        self.users = Account.create_batch(5)
        self.sites = SiteFactory.create_batch(3)
        self.subdomains = settings.SUBDOMAIN_URLCONFS
        self.languages = settings.LANGUAGES
        self.language_code = settings.LANGUAGE_CODE
        self.home = reverse('home')

    def test_language_settings_validity(self):
        """Checks that the language settings are correct.

        Open Budget expects a compliant configuration for languages.
        This test confirms that current language settings meet
        this minimum configuration requirement.
        """

        self.assertTrue(self.languages[0], self.language_code)

    def test_languages_mapped_to_subdomains(self):
        """Checks that the subdomain settings are correct.

        This test confirms the minimum requirement that each language
        in settings.LANGUAGES has a subdomain key to match.
        That's all.
        """

        for lang in self.languages:
            self.assertIn(lang[0], self.subdomains)

    def test_multilingual_metatags_presence(self):
        """Checks that the multilingual metatag partial is present.

        And, confirms that it contains an entry for each
        supported language of this Open Budget instance.
        """

        template = 'international/partials/_multilingual_meta.html'
        meta_string = '<link rel="alternate" hreflang="{lang}"'
        home = reverse('home')
        response = self.client.get(home)

        self.assertEqual(response.status_code, 200)
        # TODO: Work out how we can test for "template used", when
        # the template is loaded via a template tag
        #self.assertTemplateUsed(response, template)
        for lang in self.languages:
            self.assertContains(response, meta_string.format(lang=lang[0]))

#    def test_language_switch_presence(self):
#        """Checks that the language switch partial is present.
#
#        And, confirms that it contains an entry for each
#        supported language of this Open Budget instance.
#        """
#
#        template = 'international/partials/_language_switch.html'
#        partial_container = 'class="language-switch"'
#
#        response = self.client.get(self.home)
#
#        self.assertEqual(response.status_code, 200)
#        # TODO: Work out how we can test for "template used", when
#        # the template is loaded via a template tag
#        #self.assertTemplateUsed(response, template)
#        for _ in self.languages:
#            self.assertContains(response, partial_container)

    def test_get_language_key(self):
        """Checks that the correct language is set in the request context.


        The test covers cases where the user is both anonymous and authenticated.
        """
        for site in self.sites:
            this_subdomain = random.choice(list(self.subdomains))
            response = self.client.get("/")
            user = response.context['user']
            domain = site.domain

            if this_subdomain not in self.languages[0]:
                host = site.domain
                this_subdomain_lang = self.language_code

            else:
                host = this_subdomain + '.' + site.domain
                this_subdomain_lang = this_subdomain

            lang = get_language_key(host, domain, user)

            self.assertEqual(lang, this_subdomain_lang)

            for user in self.users:
                self.client.login(email=user.email, password='letmein')

                self.assertEqual(lang, user.language)
