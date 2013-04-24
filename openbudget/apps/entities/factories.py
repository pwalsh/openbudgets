import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.entities.models import Domain, DomainDivision, Entity


class DomainFactory(factory.Factory):

    FACTORY_FOR = Domain

    name = name = factory.Sequence(lambda n: 'Domain {0}'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class DomainDivisionFactory(factory.Factory):

    FACTORY_FOR = DomainDivision

    domain = factory.SubFactory(DomainFactory)
    index = 0
    name = name = factory.Sequence(lambda n: 'DomainDivision {0}'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class EntityFactory(factory.Factory):

    FACTORY_FOR = Entity

    division = factory.SubFactory(DomainDivisionFactory)
    name = factory.Sequence(lambda n: 'Entity {0}'.format(n))
    description = factory.Sequence(lambda n: 'Entity {0} description text.'.format(n))
    code = factory.Sequence(lambda n: 'CODE{0}'.format(n))
    parent = factory.SubFactory(EntityFactory)
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
