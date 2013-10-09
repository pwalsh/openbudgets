from fabric.api import task, local, lcd
from fabric.contrib import django
from utilities import notify, warn, alert
from config import CONFIG

django.project('openbudget')
from django.conf import settings
from django.core.management import call_command
from openbudget.apps.entities.factories import *
from openbudget.apps.sheets.factories import *
from openbudget.apps.contexts.factories import *
from openbudget.apps.transport.incoming.importers.initial import CSVImporter


@task
def bootstrap(new=False, with_env=False, with_tests=False):

    if with_env:
        update_env()

    if new:
        create_db()
    else:
        rebuild_db()

    clear_cache()
    migrate()
    init_data()

    if with_tests:
        test()


@task
def clear_cache():
    alert(u'Flushing ALL Redis keys.')
    local('redis-cli FLUSHALL')


@task
def create_db_user(name=CONFIG['db_user']):
    notify(u'Creating a new database user.')
    local('createuser --createdb {name}'.format(name=name))


@task
def create_db(user=CONFIG['db_user'], name=CONFIG['db_name']):
    notify(u'Creating a new database.')
    local('createdb --template template0 --encoding UTF-8 --owner {user} {name}'.format(user=user, name=name))


@task
def drop_db(name=CONFIG['db_name']):
    alert(u'Dropping the database.')
    local('dropdb {name}'.format(name=name))


@task
def rebuild_db(user=CONFIG['db_user'], name=CONFIG['db_name']):
    warn(u'Rebuilding the database.')
    drop_db(name)
    create_db(user, name)


@task
def update_env():
    notify(u'Updating all pip-managed and bower-managed dependencies.')
    pip_update()
    #bower_update()
    #volo_update()


@task
def migrate():
    notify(u'Running Django syncdb and migrations.')
    local('python manage.py syncdb --noinput --migrate')


@task
def init_data():
    local('python manage.py loaddata dev/sites')
    local('python manage.py loaddata locale/he/strings')
    local('python manage.py loaddata dev/interactions')
    #local('python manage.py loaddata contexts')
    #local('python manage.py loaddata dev/sources')


@task
def pip_update():
    local('pip install -U -r requirements.txt')


@task
def volo_update():
    local('volo update -f -noprompt')


@task
def bower_update():
    local('bower install')
    local('bower list')


@task
def test():
    notify(u'Running tests for the whole environment.')
    test_py()
    test_js()


@task
def test_project():
    notify(u'Running tests for project code only.')
    test_project_py()
    test_project_js()


@task
def test_py():
    notify(u'Running tests for the Python environment.')
    local('python manage.py test')


@task
def test_js():
    notify(u'Running tests for the JavaScript environment.')
    local('')


@task
def test_project_py():
    notify(u'Running tests for the project Python code.')

    project_namespace = 'openbudget.apps.'
    project_apps = []

    for app in settings.INSTALLED_APPS:
        if app.startswith(project_namespace):
            project_apps.append(app[len(project_namespace):])

    local('python manage.py test ' + ' '.join(project_apps))


@task
def test_project_js():
    notify(u'Running tests for the project JavaScript code.')
    local('')


@task
def data_clone():
    with lcd(settings.OPENBUDGETS_DATA['directory']):
        local('git clone ' + settings.OPENBUDGETS_DATA['repo'] + ' dataset')


@task
def data_fetch():
    with lcd(settings.OPENBUDGETS_DATA['directory'] + '/dataset'):
        local('git fetch')


@task
def data_merge():
    with lcd(settings.OPENBUDGETS_DATA['directory'] + '/dataset'):
        local('git merge ' + settings.OPENBUDGETS_DATA['branch'] + ' origin/'
              + settings.OPENBUDGETS_DATA['branch'])


@task
def data_load():
    CSVImporter('domain', open(settings.OPENBUDGETS_DATA['directory'] + '/dataset/data/regions/us/region.csv', 'rb'))
    CSVImporter('division', open(settings.OPENBUDGETS_DATA['directory'] + '/dataset/data/regions/us/grades/grade.csv', 'rb'))
    CSVImporter('entity', open(settings.OPENBUDGETS_DATA['directory'] + '/dataset/data/regions/us/topics/topic.csv', 'rb'))


@task
def data_upgrade():
    data_fetch()
    data_merge()


@task
def mock(amount=1000):
    notify(u'Creating some mock objects for the database.')

    domain = Domain.create(name='Example Domain')
    division = Division.create(name='Example Division', domain=domain, index=3)
    entities = Entity.create_batch(2, division=division)
    template = Template.create(name='Example Template', divisions=[division])
    template_nodes = TemplateNode.create_batch(amount)
    call_command('loaddata', 'tools')

    for node in template_nodes:
        TemplateNodeRelation.create(node=node, template=template)
        child_nodes = TemplateNode.create_batch(2, parent=node)
        for node in child_nodes:
            TemplateNodeRelation.create(node=node, template=template)

    for entity in entities:
        sheet = Sheet.create(entity=entity, template=template)
        for node in template.nodes.all():
            SheetItem.create(sheet=sheet, node=node)
