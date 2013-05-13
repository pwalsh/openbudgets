from django.test import TestCase
from openbudget.apps.contexts.factories import ContextFactory


class ContextTestCase(TestCase):

    def setUp(self):
        self.context = ContextFactory.create()

    def test_context_object(self):
        # yes, I know it is a stupid test. Need to work with these context
        # objects a bit more to see best way to test
        self.assertTrue('population' in self.context.data)
