import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.pages.models import Page


class PageFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Page

    title = factory.Sequence(lambda n: 'Page {0} Title'.format(n))
    slug = factory.Sequence(lambda n: 'page-{0}-title'.format(n))
    content = factory.Sequence(lambda n: 'Page {0} content.'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
