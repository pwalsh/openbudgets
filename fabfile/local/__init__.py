from fabric.api import task, local, roles
from fabric.contrib import django
from fabfile.utilities import notify, mock_db, sanity_check, clean_pyc
from fabfile.local import data
from fabfile.local import db
from fabfile.local import cache
from fabfile.local import env
from fabfile.config import CONFIG


@task
def bootstrap(initial='no', environment='no', cache='no'):
    notify(u'Bootstrapping the project. Hold on tight.')

    clean_up()

    # If you want to create a new database from scratch,
    # such as in a first time installation, in bootstrap, pass
    # initial=yes
    if initial == 'yes':
        db.create()
    else:
        db.rebuild()

    # If you want to check that the environment dependencies are up-to-date
    # on bootstrap, pass environment=yes
    if environment == 'yes':
        env.ensure()

    # If there is a cache in the development environment, and you
    # want it cleared on bootstrap, pass cache=yes.
    if cache == 'yes':
        cache.flush()

    migrate()


@task
def migrate():
    notify(u'Running Django syncdb and migrations.')
    local('python manage.py syncdb --noinput --migrate')
    data.init()


@task
def test():
    notify(u'Running the project test suite.')

    clean_up()

    django.project('openbudgets')
    from django.conf import settings
    project_namespace = 'openbudgets.apps.'
    project_apps = []

    for app in settings.INSTALLED_APPS:
        if app.startswith(project_namespace):
            project_apps.append(app[len(project_namespace):])

    local('python manage.py test ' + ' '.join(project_apps))


@task
def mock(amount=1000):
    notify(u'Creating some mock objects for the database.')
    mock_db(amount)


@task
def sanity():
    notify(u'Starting the project sanity check. Here come the notifications:\n')
    sanity_check()


@task
def clean_up():
    notify(u'Doing a cleanup.')
    django.project('openbudgets')
    from django.conf import settings
    clean_pyc(settings.PROJECT_ROOT + '/openbudgets')


# FOR DEPLOYMENT TO GOOGLE COMPUTE ENGINE, SET UP FIREWALLS ON THE NETWORK
# gcutil addfirewall http-web --allowed=tcp:80 --project=open-municipalities
# gcutil addfirewall https-web --allowed=:443 --project=open-municipalities


@task
@roles('web')
def new_machine():
    # just for convenience.
    #local('deactivate')
    local('gcutil addinstance ' + CONFIG['project_name'] + ' '
          '--project=open-municipalities '
          '--persistent_boot_disk '
          '--zone=europe-west1-b '
          '--external_ip_address=192.158.30.219 ' + CONFIG['machine_location'] + ' '
          '--machine_type=g1-small '
          '--ssh_user=' + CONFIG['user'] + ' '
          '--image=projects/debian-cloud/global/images/debian-7-wheezy-v20130617')


@task
@roles('web')
def delete():
    local('gcutil deleteinstance ' + CONFIG['project_name'] + ' --project=open-municipalities')
