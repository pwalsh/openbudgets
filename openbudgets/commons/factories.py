import factory
from django.contrib.sites.models import Site


class SiteFactory(factory.Factory):

    FACTORY_FOR = Site

    domain = factory.Sequence(
        lambda n: 'domain{0}.com'.format(n),)

    name = factory.Sequence(
        lambda n: 'Domain{0} Name'.format(n),)
