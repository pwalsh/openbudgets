import logging
from fabric.api import prefix, task, roles, run
from fabfile.utilities import notify
from fabfile.remote import server
from fabfile.remote import env
from fabfile.config import CONFIG, WORKON, DEACTIVATE

try:
    from sensitive import SENSITIVE
except ImportError as e:
    logging.warning('the SENSITIVE object does not exist. Creating it as an'
                    ' empty dictionary.')
    SENSITIVE = {}


@task
@roles('web')
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
@roles('web')
def upgrade():
    notify('Now starting the project upgrade sequence')
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
@roles('web')
def deploy():
    notify('Now starting the project deploy sequence')
    fetch()
    merge()
    validate()
    migrate()
    collectstatic()
    server.restart()


@task
@roles('web')
def clone():
    with prefix(WORKON):
        run('git clone ' + CONFIG['repo'] + ' .')
        run(DEACTIVATE)


@task
@roles('web')
def fetch():
    with prefix(WORKON):
        run('git fetch')
        run(DEACTIVATE)


@task
@roles('web')
def merge():
    with prefix(WORKON):
        run('git merge ' + CONFIG['branch'] + ' origin/' + CONFIG['branch'])
        run(DEACTIVATE)


@task
@roles('web')
def validate():
    with prefix(WORKON):
        run('python manage.py validate')
        run(DEACTIVATE)


@task
@roles('web')
def migrate():
    with prefix(WORKON):
        run('python manage.py syncdb --migrate')
        run(DEACTIVATE)


@task
@roles('web')
def collectstatic():
    with prefix(WORKON):
        run('python manage.py collectstatic')
        run(DEACTIVATE)


@task
@roles('web')
def command(command):
    with prefix(WORKON):
        run(command)
        run(DEACTIVATE)
    server.restart()
