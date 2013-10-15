from fabric.api import task, local
from fabfile.utilities import alert


@task
def flush():
    alert(u'Flushing ALL Redis keys.')
    local('redis-cli FLUSHALL')
