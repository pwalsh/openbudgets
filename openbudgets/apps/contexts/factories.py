import datetime
import factory
from django.utils.timezone import utc
from openbudgets.apps.entities.factories import Entity, Domain
from openbudgets.apps.contexts import models


class Context(factory.DjangoModelFactory):

    FACTORY_FOR = models.Context

    entity = factory.SubFactory(Entity)
    population = 12345
    period_start = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
    period_end = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))


class Coefficient(factory.DjangoModelFactory):

    FACTORY_FOR = models.Coefficient

    domain = factory.SubFactory(Domain)
    inflation = factory.Sequence(lambda n: '1.0{0}'.format(n))
