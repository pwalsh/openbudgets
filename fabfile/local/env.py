from fabric.api import task, local
from fabfile.utilities import notify


@task
def ensure(extended='no'):
    notify(u'Ensuring all project dependencies are present.')
    pip(extended=extended)
    #bower()
    #volo()


@task
def pip(extended='no'):
    notify(u'Ensuring all pip-managed Python dependencies are present.')
    local('pip install -U -r requirements/base.txt')
    if extended == 'yes':
        local('pip install -U -r requirements/extended.txt')


@task
def volo():
    notify(u'Ensuring all volo-managed Javascript dependencies are present.')
    local('volo update -f -noprompt')


@task
def bower():
    notify(u'Ensuring all bower-managed Javascript dependencies are present.')
    local('bower install')
    local('bower list')

