import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.entities.factories import EntityFactory, DomainFactory
from openbudget.apps.contexts import models


class ContextFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Context

    entity = factory.SubFactory(EntityFactory)
    data = '{"population":0,"ground_surface":0;"high_schools":0}'
    period_start = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
    period_end = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))


class CoefficientFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Coefficient

    domain = factory.SubFactory(DomainFactory)
    inflation = factory.Sequence(lambda n: '1.0{0}'.format(n))
