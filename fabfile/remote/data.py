from fabric.api import task, run, prefix, cd
from fabfile.utilities import notify
from fabfile.remote import db
from fabfile.config import CONFIG, WORKON, DEACTIVATE


@task
def init(environment='staging'):
    with prefix(WORKON):
        notify(u'Loading the project initial data state.')
        run('python manage.py loaddata ' + environment + '/sites')
        run('python manage.py loaddata locale/he/strings')
        run('python manage.py loaddata ' + environment + '/interactions')
        #run('python manage.py loaddata contexts')
        #run('python manage.py loaddata ' + environment +  '/sources')
        run(DEACTIVATE)


@task
def clone():
    notify(u'Cloning the data repository.')
    with prefix(WORKON), cd(CONFIG['dataset_root']):
        run('git clone ' + CONFIG['dataset_repo'] + ' dataset')
        run(DEACTIVATE)


@task
def fetch():
    notify(u'Fetching new commits from the data repository.')
    with prefix(WORKON), cd(CONFIG['dataset_root'] + '/dataset'):
        run('git fetch')
        run(DEACTIVATE)


@task
def merge():
    notify(u'Merging latest changes from the data repository.')
    with prefix(WORKON), cd(CONFIG['dataset_root'] + '/dataset'):
        run('git merge ' + CONFIG['dataset_branch'] + ' origin/' + CONFIG['dataset_branch'])
        run(DEACTIVATE)


@task
def pull():
    notify(u'Pulling latest changes from the data repository.')
    fetch()
    merge()


@task
def push():
    notify(u'Pushing latest local changes to the data repository.')
    with prefix(WORKON), cd(CONFIG['dataset_root'] + '/dataset'):
        run('git push origin/' + CONFIG['dataset_branch'])
        run(DEACTIVATE)


@task
def load(from_dump='no', source=CONFIG['db_dump_file']):
    notify(u'Loading data into the database.')
    with prefix(WORKON):

        if from_dump == 'yes':
            notify(u'Loading data from a postgresql dump source.')
            db.drop()
            db.create()
            run('psql ' + CONFIG['db_name'] + ' < ' + source)

        else:
            notify(u'Loading data from a data repository.')
            from openbudgets.apps.transport.incoming.importers.initial import CSVImporter
            CSVImporter('domain', open(CONFIG['dataset_root'] + '/dataset/data/regions/us/region.csv', 'rb'))
            CSVImporter('division', open(CONFIG['dataset_root'] + '/dataset/data/regions/us/grades/grade.csv', 'rb'))
            CSVImporter('entity', open(CONFIG['dataset_root'] + '/dataset/data/regions/us/topics/topic.csv', 'rb'))

        run(DEACTIVATE)


@task
def dump(destination=CONFIG['db_dump_file']):
    with prefix(WORKON):
        notify(u'Creating a dump of the current database.')
        run('pg_dump ' + CONFIG['db_name'] + ' > ' + destination)
        run(DEACTIVATE)


@task
def sync():
    notify(u'Syncing data to supported services.')
    with prefix(WORKON):
        from openbudgets.apps.transport.outgoing import CKANSync
        CKANSync()
        run(DEACTIVATE)
