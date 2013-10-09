import factory
from openbudgets.apps.accounts.factories import Account
from openbudgets.apps.sheets.factories import Template, TemplateNode
from openbudgets.apps.taxonomies import models


class Taxonomy(factory.DjangoModelFactory):

    FACTORY_FOR = models.Taxonomy

    user = factory.SubFactory(Account)
    template = factory.Subfactory(Template)
    name = factory.Sequence(lambda n: 'Taxonomy {0}'.format(n))
    description = factory.Sequence(lambda n: 'Taxononmy {0} description text.'.format(n))


class Tag(factory.DjangoModelFactory):

    FACTORY_FOR = models.Tag

    taxonomy = factory.SubFactory(Taxonomy)
    name = factory.Sequence(lambda n: 'Taxonomy {0}'.format(n))


class TaggedNode(factory.DjangoModelFactory):

    FACTORY_FOR = models.TaggedNode

    tag = factory.SubFactory(Tag)
    content_object = factory.SubFactory(TemplateNode)
