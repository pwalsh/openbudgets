import logging
import cuisine
from fabric.api import task, roles, run, prefix
from fabfile import templates
from fabfile.utilities import notify
from fabfile.config import CONFIG, WORKON, DEACTIVATE

try:
    from sensitive import SENSITIVE
except ImportError as e:
    logging.warning(u'the SENSITIVE object does not exist. Creating it as an'
                    u' empty dictionary.')
    SENSITIVE = {}


@task
@roles('demo')
def ensure():
    notify(u'Ensuring all project dependencies are present.')
    pip()
    #bower()
    #volo()


def make():
    run('mkvirtualenv ' + CONFIG['project_name'])
    cuisine.dir_ensure(CONFIG['project_root'])
    run('setvirtualenvproject ' + CONFIG['project_env'] + ' ' + CONFIG['project_root'])


@task
@roles('demo')
def settings():
    notify(u'Configuring production settings.')
    with prefix(WORKON):
        context = CONFIG
        context.update(SENSITIVE)
        content = cuisine.text_template(templates.production_settings, context)
        cuisine.file_write(CONFIG['project_root'] + '/openbudgets/settings/production.py',
                           content)
        run(DEACTIVATE)


@task
@roles('demo')
def pip():
    notify(u'Ensuring all pip-managed Python dependencies are present.')
    with prefix(WORKON):
        run('pip install -U -r requirements/base.txt')
        run('pip install -U -r requirements/extended.txt')
        run(DEACTIVATE)


@task
@roles('demo')
def volo():
    notify(u'Ensuring all volo-managed Javascript dependencies are present.')
    with prefix(WORKON):
        run('volo update -f -noprompt')
        run(DEACTIVATE)


@task
@roles('demo')
def bower():
    notify(u'Ensuring all bower-managed Javascript dependencies are present.')
    with prefix(WORKON):
        run('bower install')
        run('bower list')
        run(DEACTIVATE)
