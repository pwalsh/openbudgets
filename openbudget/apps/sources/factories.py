import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.accounts.factories import AccountFactory
from openbudget.apps.sources.models import ReferenceSource, AuxSource


class DataSourceFactory(factory.Factory):

    added_by = factory.SubFactory(AccountFactory)
    name = factory.Sequence(lambda n: 'Data Source Name {0}'.format(n))
    url = factory.Sequence(lambda n: 'http://www{0}.example.com/'.format(n))
    retrieval_date = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    notes = factory.Sequence(lambda n: 'The notes for Data Source {0}'.format(n))
    content_type = 1
    object_id = 1
    last_login = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    date_joined = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class ReferenceSourceFactory(DataSourceFactory):
    FACTORY_FOR = ReferenceSource


class AuxSourceFactory(DataSourceFactory):
    FACTORY_FOR = AuxSource
