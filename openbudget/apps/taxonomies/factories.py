import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.accounts.factories import AccountFactory
from openbudget.apps.budgets.factories import BudgetTemplateFactory
from openbudget.apps.taxonomies.models import Taxonomy, Tag, TaggedNode


class TaxonomyFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Taxonomy

    user = factory.SubFactory(AccountFactory)
    template = factory.Subfactory(BudgetTemplateFactory)
    name = factory.Sequence(lambda n: 'Taxonomy {0}'.format(n))
    description = factory.Sequence(lambda n: 'Taxononmy {0} description text.'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class TagFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Tag

    taxonomy = factory.SubFactory(TaxonomyFactory)
    name = factory.Sequence(lambda n: 'Taxonomy {0}'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class TaggedNodeFactory(factory.DjangoModelFactory):

    FACTORY_FOR = TaggedNode

    tag = factory.SubFactory(TagFactory)
    content_object = factory.SubFactory(BudgetTemplateNode)
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
