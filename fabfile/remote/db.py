from fabric.api import task, sudo, run, roles
from fabfile.utilities import notify, warn, alert
from fabfile.config import CONFIG


@task
@roles('demo')
def create(user=CONFIG['db_user'], name=CONFIG['db_name']):
    notify(u'Creating a new database.')
    run('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=user, name=name))


@task
@roles('demo')
def drop(name=CONFIG['db_name']):
    alert(u'Dropping the database.')
    run('dropdb {name}'.format(name=name))


@task
@roles('demo')
def rebuild(user=CONFIG['db_user'], name=CONFIG['db_name']):
    warn(u'Rebuilding the database.')
    drop(name)
    create(user, name)


@task
@roles('demo')
def createuser(name=CONFIG['db_user']):
    notify(u'Creating a new database user.')
    run('createuser --createdb {name}'.format(name=name))
