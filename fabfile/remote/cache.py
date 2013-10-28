from fabric.api import task, sudo, roles
from fabfile.utilities import alert


@task
@roles('demo')
def flush():
    alert(u'Flushing ALL Redis keys.')
    sudo('redis-cli FLUSHALL')
