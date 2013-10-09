import factory
from openbudgets.apps.pages import models


class Page(factory.DjangoModelFactory):

    FACTORY_FOR = models.Page

    title = factory.Sequence(lambda n: 'Page {0} Title'.format(n))
    slug = factory.Sequence(lambda n: 'page-{0}-title'.format(n))
    content = factory.Sequence(lambda n: 'Page {0} content.'.format(n))
