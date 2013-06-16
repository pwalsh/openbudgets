import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.entities.models import Domain, Division, Entity


class DomainFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Domain

    name = name = factory.Sequence(lambda n: 'Domain {0}'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class DivisionFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Division

    domain = factory.SubFactory(DomainFactory)
    index = 0
    name = name = factory.Sequence(lambda n: 'DomainDivision {0}'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class EntityFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Entity

    division = factory.SubFactory(DivisionFactory)
    name = factory.Sequence(lambda n: 'Entity {0}'.format(n))
    slug = factory.Sequence(lambda n: 'entity-{0}'.format(n))
    description = factory.Sequence(lambda n: 'Entity {0} description text.'.format(n))
    code = factory.Sequence(lambda n: 'CODE{0}'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
