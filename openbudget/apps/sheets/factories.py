import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.entities.factories import EntityFactory
from openbudget.apps.sheets import models


class TemplateFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Template

    name = factory.Sequence(lambda n: 'Template {0}'.format(n))
    description = factory.Sequence(lambda n: 'Template {0} description text.'.format(n))
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


class TemplateNodeFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.TemplateNode

    directions = models.TemplateNode.DIRECTIONS

    code = factory.Sequence(lambda n: '{0}'.format(n))
    name = factory.Sequence(lambda n: 'Budget Template Node {0} Name'.format(n))
    description = factory.Sequence(lambda n: 'Budget Template Node {0} description.'.format(n))
    direction = directions[0][0]
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )

    @classmethod
    def _prepare(cls, create, **kwargs):
        template = TemplateFactory()
        btnode = super(TemplateNodeFactory, cls)._prepare(create, **kwargs)
        btnode.templates.add(template)
        return btnode


class TemplateNodeRelationFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.TemplateNodeRelation

    template = factory.SubFactory(TemplateFactory)
    node = factory.SubFactory(TemplateNodeFactory)


class SheetFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Sheet

    entity = factory.SubFactory(EntityFactory)
    template = factory.SubFactory(TemplateFactory)
    description = factory.Sequence(lambda n: 'Sheet Factory {0} description.'.format(n))
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


class SheetItemFactory(factory.Factory):

    FACTORY_FOR = models.SheetItem

    node = factory.SubFactory(TemplateNodeFactory)
    description = factory.Sequence(lambda n: 'Sheet Item Factory {0} description.'.format(n))
    budget = 20000
    actual = 20000
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
