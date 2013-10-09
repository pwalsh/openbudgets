import factory
from openbudgets.apps.entities import models


class Domain(factory.DjangoModelFactory):

    FACTORY_FOR = models.Domain

    name = name = factory.Sequence(lambda n: 'Domain {0}'.format(n))


class Division(factory.DjangoModelFactory):

    FACTORY_FOR = models.Division

    domain = factory.SubFactory(Domain)
    index = 0
    name = name = factory.Sequence(lambda n: 'DomainDivision {0}'.format(n))


class Entity(factory.DjangoModelFactory):

    FACTORY_FOR = models.Entity

    division = factory.SubFactory(Division)
    name = factory.Sequence(lambda n: 'Entity {0}'.format(n))
    slug = factory.Sequence(lambda n: 'entity-{0}'.format(n))
    description = factory.Sequence(lambda n: 'Entity {0} description text.'.format(n))
    code = factory.Sequence(lambda n: 'CODE{0}'.format(n))
