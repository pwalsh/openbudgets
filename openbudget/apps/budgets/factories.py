import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.entities.factories import EntityFactory, DomainDivisionFactory
from openbudget.apps.budgets.models import BudgetTemplate, BudgetTemplateNode, BudgetTemplateNodeRelation, Sheet, Budget, Actual, SheetItem, BudgetItem, ActualItem


class BudgetTemplateFactory(factory.DjangoModelFactory):

    FACTORY_FOR = BudgetTemplate

    name = factory.Sequence(lambda n: 'Budget Template {0}'.format(n))
    description = factory.Sequence(lambda n: 'Budget Template {0} description text.'.format(n))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )

    @factory.post_generation
    def divisions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for division in extracted:
                self.divisions.add(division)


class BudgetTemplateNodeFactory(factory.DjangoModelFactory):

    FACTORY_FOR = BudgetTemplateNode

    directions = BudgetTemplateNode.NODE_DIRECTIONS

    code = factory.Sequence(lambda n: '{0}'.format(n))
    name = factory.Sequence(lambda n: 'Budget Template Node {0} Name'.format(n))
    description = factory.Sequence(lambda n: 'Budget Template Node {0} description.'.format(n))
    #parent = factory.SubFactory(BudgetTemplateNodeFactory)
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
        template = BudgetTemplateFactory()
        btnode = super(BudgetTemplateNodeFactory, cls)._prepare(create, **kwargs)
        btnode.templates.add(template)
        return btnode


class BudgetTemplateNodeRelationFactory(factory.DjangoModelFactory):

    FACTORY_FOR = BudgetTemplateNodeRelation

    template = factory.SubFactory(BudgetTemplateFactory)
    node = factory.SubFactory(BudgetTemplateNodeFactory)


class SheetFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Sheet

    entity = factory.SubFactory(EntityFactory)
    template = factory.SubFactory(BudgetTemplateFactory)
    description = factory.Sequence(lambda n: 'Budget Factory {0} description.'.format(n))
    period_start = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc).date()
    )
    period_end = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc).date()
    )
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class BudgetFactory(SheetFactory):

    FACTORY_FOR = Budget


class ActualFactory(SheetFactory):

    FACTORY_FOR = Actual


class SheetItemFactory(factory.Factory):

    FACTORY_FOR = SheetItem

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
