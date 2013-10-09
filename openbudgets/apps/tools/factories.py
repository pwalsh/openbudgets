import factory
from openbudgets.apps.tools import models
from openbudgets.apps.accounts.factories import Account


class Tool(factory.DjangoModelFactory):

    FACTORY_FOR = models.Tool

    user = factory.SubFactory(Account)
    name = factory.Sequence(lambda n: 'Tool Name {0}'.format(n))
    author = factory.SubFactory(Account)
    description = factory.Sequence(lambda n: 'Tool description {0}.'.format(n))
    label = 'public'
    featured = True
    config = {"key": "value"}


class State(factory.DjangoModelFactory):

    FACTORY_FOR = models.State

    tool = factory.SubFactory(Tool)
    author = factory.SubFactory(Account)
    config = {"key": "value"}
