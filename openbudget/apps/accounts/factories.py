import datetime
import factory
from django.utils.timezone import utc
from openbudget.apps.accounts.models import Account


class AccountFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Account
    password = 'letmein'

    email = factory.Sequence(lambda n: 'p{0}@here.com'.format(n))
    first_name = factory.Sequence(lambda n: 'first_name{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'last_name{0}'.format(n))
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
    created_on = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))
    last_modified = factory.Sequence(
        lambda n: datetime.datetime.utcnow().replace(tzinfo=utc))

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        account = super(AccountFactory, cls)._prepare(create, **kwargs)
        account.set_password(password)
        if create:
            account.save()
        return account
