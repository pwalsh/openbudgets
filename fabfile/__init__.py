from quilt import *
from dock.fabfile import *


from fabric.api import task, env, execute, roles
from fabric import operations
from quilt.remote.db import rebuild


@roles('db')
@task
def db_put():
    utilities.notify(u'Loading a local db dump to the remote dump location.')

    execute(rebuild)

    operations.put('/Users/paulwalsh/Sites/projects/openbudgets/tmp/db_dump.sql',
                   '/srv/projects/openbudgets/tmp/db_dump.sql')
