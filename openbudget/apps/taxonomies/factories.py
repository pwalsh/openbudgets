import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.accounts.factories import AccountFactory
from openbudget.apps.budgets.factories import BudgetTemplateFactory
from openbudget.apps.taxonomies.models import Taxonomy, Tag, TaggedNode


class TaxonomyFactory(factory.Factory):

    FACTORY_FOR = Account

    user = factory.SubFactory(AccountFactory)
    template = factory.Subfactory(BudgettemplateFactory)
    name = factory.Sequence(lambda n: 'Taxonomy {0}'.format(n))
    description = factory.Sequence(lambda n: 'Taxononmy {0} description text.'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
