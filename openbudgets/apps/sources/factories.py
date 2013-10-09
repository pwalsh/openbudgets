import datetime
import factory
from django.utils.timezone import utc
from openbudgets.apps.accounts.factories import Account
from openbudgets.apps.sources import models


class DataSource(factory.DjangoModelFactory):

    added_by = factory.SubFactory(Account)
    name = factory.Sequence(lambda n: 'Data Source Name {0}'.format(n))
    url = factory.Sequence(lambda n: 'http://www{0}.example.com/'.format(n))
    retrieval_date = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
    notes = factory.Sequence(lambda n: 'The notes for Data Source {0}'.format(n))


class ReferenceSource(DataSource):
    FACTORY_FOR = models.ReferenceSource


class AuxSource(DataSource):
    FACTORY_FOR = models.AuxSource
