import logging
from fabric.api import prefix, task, roles, run
from fabric.contrib import django
from fabfile.utilities import notify, mock_db, clean_pyc, sanity_check
from fabfile.remote import server
from fabfile.remote import env
from fabfile.remote import db
from fabfile.remote import data
from fabfile.remote import cache
from fabfile.config import CONFIG, WORKON, DEACTIVATE

try:
    from fabfile.sensitive import SENSITIVE
except ImportError as e:
    logging.warning(u'the SENSITIVE object does not exist. Creating it as an'
                    u' empty dictionary.')
    SENSITIVE = {}


@task
@roles('demo')
def bootstrap():
    notify(u'Now starting the project bootstrap sequence')
    env.make()
    clone()
    env.ensure()
    env.settings()
    validate()
    migrate()
    collectstatic()
    server.nginx()
    server.gunicorn()
    #server.celery()


@task
@roles('demo')
def upgrade():
    notify(u'Now starting the project upgrade sequence')
    fetch()
    merge()
    env.ensure()
    env.settings()
    validate()
    migrate()
    collectstatic()
    server.nginx()
    server.gunicorn()
    #server.celery()


@task
@roles('demo')
def deploy():
    notify(u'Now starting the project deploy sequence')
    fetch()
    merge()
    validate()
    migrate()
    collectstatic()
    server.restart()


@task
@roles('demo')
def clone():
    with prefix(WORKON):
        run('git clone ' + CONFIG['repo'] + ' .')
        run(DEACTIVATE)


@task
@roles('demo')
def fetch():
    with prefix(WORKON):
        run('git fetch')
        run(DEACTIVATE)


@task
@roles('demo')
def merge():
    with prefix(WORKON):
        run('git merge ' + CONFIG['branch'] + ' origin/' + CONFIG['branch'])
        run(DEACTIVATE)


@task
@roles('demo')
def validate():
    with prefix(WORKON):
        run('python manage.py validate')
        run(DEACTIVATE)


@task
@roles('demo')
def migrate():
    with prefix(WORKON):
        run('python manage.py syncdb --migrate')
        data.init()
        run(DEACTIVATE)


@task
@roles('demo')
def collectstatic():
    with prefix(WORKON):
        run('python manage.py collectstatic')
        run(DEACTIVATE)


@task
@roles('demo')
def command(cmd):
    with prefix(WORKON):
        run(cmd)
        run(DEACTIVATE)
    server.restart()


@task
def mock(amount=1000):
    notify(u'Creating some mock objects for the database.')
    with prefix(WORKON):
        mock_db(amount)
        run(DEACTIVATE)
    server.restart()


@task
def sanity():
    notify(u'Starting the project sanity check. Here come the notifications:\n')
    sanity_check()


@task
def clean_up():
    notify(u'Doing a cleanup.')
    django.project(CONFIG['project_name'])
    from django.conf import settings
    clean_pyc(settings.PROJECT_ROOT + '/' + CONFIG['project_name'])
