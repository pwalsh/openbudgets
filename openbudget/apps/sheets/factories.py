import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.entities.factories import EntityFactory
from openbudget.apps.accounts.factories import AccountFactory
from openbudget.apps.sheets import models


class TemplateFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Template

    name = factory.Sequence(lambda n: 'Template {0}'.format(n))
    description = factory.Sequence(lambda n: 'Template {0} desc...'.format(n))
    period_start = factory.Sequence(lambda n: datetime.datetime.utcnow()
                                    .replace(month=1, day=1, tzinfo=utc)
                                    .date(),)

    @factory.post_generation
    def divisions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for division in extracted:
                self.divisions.add(division)


class TemplateNodeFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.TemplateNode

    name = factory.Sequence(lambda n: 'Template Node {0} name'.format(n))
    code = factory.Sequence(lambda n: '{0}'.format(n))
    comparable = True
    direction = 'REVENUE'
    description = factory.Sequence(lambda n: 'Template Node {0} description.'.format(n))

    @factory.post_generation
    def inverse(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for inverse in extracted:
                self.inverse.add(inverse)

    @factory.post_generation
    def backwards(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for node in extracted:
                self.backwards.add(node)


class TemplateNodeRelationFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.TemplateNodeRelation

    template = factory.SubFactory(TemplateFactory)
    node = factory.SubFactory(TemplateNodeFactory)


class SheetFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Sheet

    entity = factory.SubFactory(EntityFactory)
    template = factory.SubFactory(TemplateFactory)
    budget = 20000
    actual = 22000
    description = factory.Sequence(lambda n: 'Sheet Factory {0} description.'.format(n))
    period_start = factory.Sequence(lambda n: datetime.datetime.utcnow()
                                    .replace(month=1, day=1, tzinfo=utc)
                                    .date(),)
    period_end = factory.Sequence(lambda n: datetime.datetime.utcnow()
                                  .replace(month=12, day=31, tzinfo=utc)
                                  .date(),)


class SheetItemFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.SheetItem

    sheet = factory.SubFactory(SheetFactory)
    node = factory.SubFactory(TemplateNodeFactory)
    description = factory.Sequence(lambda n: 'Sheet Item desc {0}'.format(n))
    budget = 20000
    actual = 22000


class SheetItemCommentFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.SheetItemComment

    item = factory.SubFactory(SheetItemFactory)
    user = factory.SubFactory(AccountFactory)
    comment = factory.Sequence(lambda n: 'Sheet Item Comment {0}.'.format(n))
