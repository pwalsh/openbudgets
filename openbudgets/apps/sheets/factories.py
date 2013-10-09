import datetime
import factory
from django.utils.timezone import utc
from openbudgets.apps.entities.factories import Entity
from openbudgets.apps.accounts.factories import Account
from openbudgets.apps.sheets import models


class Template(factory.DjangoModelFactory):

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


class TemplateNode(factory.DjangoModelFactory):

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


class TemplateNodeRelation(factory.DjangoModelFactory):

    FACTORY_FOR = models.TemplateNodeRelation

    template = factory.SubFactory(Template)
    node = factory.SubFactory(TemplateNode)


class Sheet(factory.DjangoModelFactory):

    FACTORY_FOR = models.Sheet

    entity = factory.SubFactory(Entity)
    template = factory.SubFactory(Template)
    budget = 20000
    actual = 22000
    description = factory.Sequence(lambda n: 'Sheet Factory {0} description.'.format(n))
    period_start = factory.Sequence(lambda n: datetime.datetime.utcnow()
                                    .replace(month=1, day=1, tzinfo=utc)
                                    .date(),)
    period_end = factory.Sequence(lambda n: datetime.datetime.utcnow()
                                  .replace(month=12, day=31, tzinfo=utc)
                                  .date(),)


class SheetItem(factory.DjangoModelFactory):

    FACTORY_FOR = models.SheetItem

    sheet = factory.SubFactory(Sheet)
    node = factory.SubFactory(TemplateNode)
    description = factory.Sequence(lambda n: 'Sheet Item desc {0}'.format(n))
    budget = 20000
    actual = 22000


class SheetItemComment(factory.DjangoModelFactory):

    FACTORY_FOR = models.SheetItemComment

    item = factory.SubFactory(SheetItem)
    user = factory.SubFactory(Account)
    comment = factory.Sequence(lambda n: 'Sheet Item Comment {0}.'.format(n))
