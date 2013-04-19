import datetime
from django.utils.timezone import utc
import factory
from django.contrib.auth.models import User
from openbudget.settings import base as settings
from openbudget.apps.accounts.models import Account


class UserFactory(factory.Factory):

    FACTORY_FOR = User
    password = 'letmein'

    username = factory.Sequence(lambda n: 'username{0}'.format(n))
    email = factory.Sequence(lambda n: 'p{0}@here.com'.format(n))
    first_name = factory.Sequence(lambda n: 'first_name{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'last_name{0}'.format(n))
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )
    date_joined = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc)
    )

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        user.set_password(password)
        if create:
            user.save()
        return user


class AccountFactory(factory.Factory):

    FACTORY_FOR = Account

    user = factory.SubFactory(UserFactory)
    language = settings.LANGUAGE_CODE
