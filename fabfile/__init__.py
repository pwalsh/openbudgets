from fabric.api import task

from fabric.contrib import django
django.project('openbudgets')

from quilt import e, local, remote, contrib, utilities
from dock.fabfile import dock


@task
def mock(amount=300):
    utilities.notify(u'Creating some mock objects for the database.')
    from openbudgets.commons.data import mock_db
    mock_db(amount)
