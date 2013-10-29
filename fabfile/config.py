import datetime
from fabric.api import env
from fabric.contrib import django
django.project('openbudgets')
from django.conf import settings

env.user = 'robot'
env.roledefs = {
    'demo': ['162.243.15.220'],
    'openmuni-budgets': [''],
}


CONFIG = {
    'debug': True,
    'sentry_dsn': '',
    'user': env.user,
    'machine_location': env.roledefs['demo'][0],
    'machine_port': 80,
    'project_name': 'openbudgets',
    'project_root': '/srv/projects/openbudgets',
    'project_env': '/srv/environments/openbudgets',
    'dataset_root': settings.OPENBUDGETS_DATA['directory'],
    'dataset_repo': settings.OPENBUDGETS_DATA['repo'],
    'dataset_branch': settings.OPENBUDGETS_DATA['branch'],
    'db_name': 'openbudgets',
    'db_user': env.user,
    'db_dump_file': settings.OPENBUDGETS_DATA['db_dump'],
    'app_location': '127.0.0.1',
    'app_port': 9000,
    'app_workers': 4,
    'app_timeout': 150,
    'app_wsgi': 'openbudgets.wsgi:application',
    'queue_workers': 2,
    'queue_max_tasks_per_child': 10,
    'queue_log': '/srv/logs/openbudgets_celery.log',
    'repo': 'https://github.com/prjts/openbudgets',
    'branch': 'develop',
    'allowed_hosts': ['openbudgets.io', 'en.openbudgets.io', 'he.openbudgets.io',
                      'ar.openbudgets.io','ru.openbudgets.io'],
    'cookie_domain': '.openbudgets.io',
    'nginx_access_log': '/srv/logs/openbudgets_nginx_access.log',
    'nginx_error_log': '/srv/logs/openbudgets_nginx_error.log',
    'gunicorn_access_log': '/srv/logs/openbudgets_gunicorn_access.log',
    'gunicorn_error_log': '/srv/logs/openbudgets_gunicorn_error.log',
    'redis_access_log': '/srv/logs/openbudgets_redis_access.log',
    'redis_error_log': '/srv/logs/openbudgets_redis_error.log',
    'timestamp': datetime.datetime.now(),
}

WORKON = 'workon ' + CONFIG['project_name']

DEACTIVATE = 'deactivate'
