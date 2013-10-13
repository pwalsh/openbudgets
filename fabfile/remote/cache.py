from fabric.api import task, sudo
from fabfile.utilities import alert


@task
def flush():
    alert(u'Flushing ALL Redis keys.')
    sudo('redis-cli FLUSHALL')
