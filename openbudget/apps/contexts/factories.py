import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.entities.factories import EntityFactory
from openbudget.apps.contexts.models import Context


class ContextFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Context

    entity = factory.SubFactory(EntityFactory)
    data = '{"population":0,"ground_surface":0;"high_schools":0}'
    period_start = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
    period_end = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
