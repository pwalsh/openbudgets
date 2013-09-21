import datetime
import factory
from django.utils.timezone import utc
#from django.contrib.contenttypes.models import ContentType
from openbudget.apps.accounts.factories import Account
from openbudget.apps.interactions import models


class Interaction(factory.DjangoModelFactory):
    FACTORY_FOR = models.Interaction

    user = factory.SubFactory(Account)


class Star(Interaction):
    FACTORY_FOR = models.Star


class Follow(Interaction):
    FACTORY_FOR = models.Follow


class Share(Interaction):
    FACTORY_FOR = models.Share
