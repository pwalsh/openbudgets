import datetime
import factory
from django.utils.timezone import utc
#from django.contrib.contenttypes.models import ContentType
from openbudget.apps.accounts.factories import AccountFactory
from openbudget.apps.interactions.models import Star, Follow, Share


class InteractionFactory(factory.DjangoModelFactory):

    user = factory.SubFactory(AccountFactory)
    content_type = 1
    object_id = 1
    last_login = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    date_joined = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )


class StarFactory(InteractionFactory):
    FACTORY_FOR = Star


class FollowFactory(InteractionFactory):
    FACTORY_FOR = Follow


class ShareFactory(InteractionFactory):
    FACTORY_FOR = Share
