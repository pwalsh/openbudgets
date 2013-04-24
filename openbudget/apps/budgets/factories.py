import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.entities.factories import EntityFactory, DomainDivisionFactory
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode, BudgetTemplateNodeRelation, Budget, Actual, BudgetItem, ActualItem


class BudgetTemplateFactory(factory.Factory):

    FACTORY_FOR = BudgetTemplate

    division = factory.SubFactory(DomainDivisionFactory)
    name = factory.Sequence(lambda n: 'Budget Template {0}'.format(n))
    description = factory.Sequence(lambda n: 'Budget Template {0} description text.'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class BudgetTemplateNodeFactory(factory.Factory):

    FACTORY_FOR = BudgetTemplateNode

    directions = BudgetTemplateNode.NODE_DIRECTIONS

    code = factory.Sequence(lambda n: '{0}'.format(n))
    name = factory.Sequence(lambda n: 'Budget Template Node {0} Name'.format(n))
    description = factory.Sequence(lambda n: 'Budget Template Node {0} description.'.format(n))
    parent = factory.SubFactory(BudgetTemplateNodeFactory)
    #backwards =
    direction = directions[0][0]
    #inverse =
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )

    @classmethod
    def _prepare(cls, create, **kwargs):


        # DO TEMPLATES M2M


        #password = kwargs.pop('password', None)
        #account = super(AccountFactory, cls)._prepare(create, **kwargs)
        #account.set_password(password)
        #if create:
        #    account.save()
        value = True
        return value


class BudgetTemplateNodeRelationFactory(factory.Factory):

    FACTORY_FOR = BudgetTemplateNodeRelation

    template = factory.SubFactory(BudgetTemplateFactory)
    node = factory.SubFactory(BudgetTemplateNodeFactory)


class SheetFactory(factory.Factory):

    entity = factory.SubFactory(EntityFactory)
    template = factory.SubFactory(BudgetTemplateFactory)
    description = factory.Sequence(lambda n: 'Budget Factory {0} description.'.format(n))
    period_start = factory.Sequence(
        lambda n: datetime.date.utcnow().replace(tzinfo=utc)
    )
    period_end = factory.Sequence(
        lambda n: datetime.date.utcnow().replace(tzinfo=utc)
    )
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class BudgetFactory(SheetFactory):

    FACTORY_FOR = Actual


class ActualFactory(SheetFactory):

    FACTORY_FOR = Actual


class SheetItemFactory(factory.Factory):

    node = factory.SubFactory(BudgetTemplateNodeFactory)
    description = factory.Sequence(lambda n: 'Budget Factory {0} description.'.format(n))
    amount = 20000
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class ActualItemFactory(SheetItemFactory):

    FACTORY_FOR = ActualItem

    actual = factory.SubFactory(ActualFactory)


class BudgetItemFactory(SheetItemFactory):

    FACTORY_FOR = BudgetItem

    budget = factory.SubFactory(BudgetFactory)
