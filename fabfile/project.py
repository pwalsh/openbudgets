import logging
import cuisine
from fabric.api import prefix, task, roles, run, sudo
from utilities import notify
import templates
from conf import PROJECT, MACHINE, KEY

try:
    from sensitive import SENSITIVE
except ImportError as e:
    logging.warning('the SENSITIVE object does not exist. Creating it as an'
                    ' empty dictionary.')
    SENSITIVE = {}


WORKON = 'workon ' + KEY
DEACTIVATE = 'deactivate'


@task
@roles('web')
def bootstrap():
    notify('Now starting the project bootstrap sequence')
    make_environment()
    clone()
    ensure_dependencies()
    validate()
    migrate()
    collectstatic()
    ensure_production_settings()
    ensure_nginx()
    ensure_gunicorn()
    ensure_celery()


@task
@roles('web')
def upgrade():
    notify('Now starting the project upgrade sequence')
    fetch()
    merge()
    ensure_dependencies()
    validate()
    migrate()
    collectstatic()
    ensure_production_settings()
    ensure_nginx()
    ensure_gunicorn()
    ensure_celery()


@task
@roles('web')
def clone():
    with prefix(WORKON):
        run('git clone ' + PROJECT['REPO'] + ' .')
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
        run('git merge ' + PROJECT['BRANCH'] + ' origin/' + PROJECT['BRANCH'])
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
def restart():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl restart ' + KEY + '-gunicorn')
    sudo('supervisorctl restart ' + KEY + '-celery')


@task
@roles('web')
def start():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl start ' + KEY + '-gunicorn')
    sudo('supervisorctl start ' + KEY + '-celery')


@task
@roles('web')
def stop():
    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl stop ' + KEY + '-gunicorn')
    sudo('supervisorctl stop ' + KEY + '-celery')


@task
@roles('web')
def ensure_dependencies():
    from_pip()
    from_volo()


def from_pip():
    with prefix(WORKON):
        run('pip install -U -r requirements/base.txt')
        run('pip install -U -r requirements/deploy.txt')
        run(DEACTIVATE)


def from_volo():
    with prefix(WORKON):
        run('volo add -noprompt')
        run(DEACTIVATE)


def make_environment():
    run('mkvirtualenv ' + KEY)
    cuisine.dir_ensure(PROJECT['ROOT'])
    run('setvirtualenvproject ' + MACHINE['DIR_ENVIRONMENTS'] + '/' + KEY + ' '
        + MACHINE['DIR_PROJECTS'] + '/' + KEY)


@task
@roles('web')
def ensure_production_settings():
    notify('Configuring production settings.')
    context = SENSITIVE
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.production_settings, context)
    cuisine.file_write(PROJECT['ROOT'] + '/openbudget/settings/production.py',
                       content)
    restart()


@task
@roles('web')
def ensure_nginx():
    notify('Configuring nginx.')
    context = {
        'ACTION_DATE': MACHINE['ACTION_DATE'],
        'NAME': PROJECT['NAME'],
        'KEY': KEY,
        'APP_LOCATION': PROJECT['APP_LOCATION'],
        'APP_PORT': PROJECT['APP_PORT'],
        'LOCATION': MACHINE['LOCATION'],
        'PORT': MACHINE['PORT'],
        'PROJECT_ROOT': PROJECT['ROOT'],
        'ACCESS_LOG': PROJECT['LOGS']['NGINX_ACCESS'],
        'ERROR_LOG': PROJECT['LOGS']['NGINX_ERROR'],
        'SERVER_NAMES': ' '.join(PROJECT['DOMAINS'])
    }
    cuisine.mode_sudo()
    content = cuisine.text_template(templates.nginx, context)
    cuisine.file_write('/etc/nginx/sites-enabled/' + KEY, content)
    sudo('/etc/init.d/nginx restart')


@task
@roles('web')
def ensure_gunicorn():
    notify('Configuring gunicorn.')
    context = {
        'ACTION_DATE': MACHINE['ACTION_DATE'],
        'NAME': PROJECT['NAME'],
        'KEY': KEY,
        'APP_LOCATION': PROJECT['APP_LOCATION'],
        'APP_PORT': PROJECT['APP_PORT'],
        'APP_WSGI': PROJECT['APP_WSGI'],
        'APP_WORKERS': PROJECT['APP_WORKERS'],
        'LOCATION': MACHINE['LOCATION'],
        'PORT': MACHINE['PORT'],
        'PROJECT_ROOT': PROJECT['ROOT'],
        'PROJECT_ENV': PROJECT['ENV'],
        'ACCESS_LOG': PROJECT['LOGS']['GUNICORN_ACCESS'],
        'ERROR_LOG': PROJECT['LOGS']['GUNICORN_ERROR'],
    }

    cuisine.mode_sudo()
    content = cuisine.text_template(templates.gunicorn_supervisor, context)
    cuisine.file_write('/etc/supervisor/conf.d/' + KEY + '-gunicorn.conf', content)
    restart()


@task
@roles('web')
def ensure_celery():
    notify('Configuring celery.')
    context = {
        'ACTION_DATE': MACHINE['ACTION_DATE'],
        'NAME': PROJECT['NAME'],
        'KEY': KEY,
        'CONCURRENCY': PROJECT['CELERY_CONCURRENCY'],
        'MAX_TASKS_PER_CHILD': PROJECT['CELERY_MAX_TASKS_PER_CHILD'],
        'PROJECT_ROOT': PROJECT['ROOT'],
        'PROJECT_ENV': PROJECT['ENV'],
        'ACCESS_LOG': PROJECT['LOGS']['CELERY'],
    }

    cuisine.mode_sudo()
    content = cuisine.text_template(templates.celery_supervisor, context)
    cuisine.file_write('/etc/supervisor/conf.d/' + KEY + '-celery.conf', content)
    restart()


@task
@roles('web')
def db_load():
    notify('Loading data to postgres.')
    local = '/Users/paulwalsh/Desktop/postgres_9.1.sql'
    remote = MACHINE['DIR_USER_HOME'] + '/' + KEY + '.sql'
    cuisine.file_upload(remote, local)
    run('dropdb ' + KEY)
    run('createdb ' + KEY)
    run('psql ' + KEY + ' < ' + remote)
