import datetime
from fabric.api import env
from fabric.contrib import django
django.project('openbudgets')
from django.conf import settings

env.user = 'robot'
env.roledefs = {
    'web': ['192.158.30.219']
}


CONFIG = {
    'sentry_dsn': '',
    'user': env.user,
    'machine_location': env.roledefs['web'][0],
    'machine_port': 80,
    'project_name': 'open-budgets',
    'project_root': '/srv/projects/open-budgets',
    'project_env': '/srv/environments/open-budgets',
    'dataset_root': settings.OPENBUDGETS_DATA['directory'],
    'dataset_repo': settings.OPENBUDGETS_DATA['repo'],
    'dataset_branch': settings.OPENBUDGETS_DATA['branch'],
    'db_name': 'openbudgets',
    'db_user': env.user,
    'db_dump_file': settings.OPENBUDGETS_DATA['db_dump'],
    'app_location': '127.0.0.1',
    'app_port': 9000,
    'app_workers': 4,
    'app_timeout': 45,
    'app_wsgi': 'openbudget.wsgi:application',
    'repo': 'https://github.com/hasadna/openmuni-budgets',
    'branch': 'develop',
    'allowed_hosts': ['dev.openmuni.org.il', 'api.dev.openmuni.org.il',
                      'en.dev.openmuni.org.il', 'he.dev.openmuni.org.il',
                      'ar.dev.openmuni.org.il', 'ru.dev.openmuni.org.il'],
    'cookie_domain': '.openmuni.org.il',
    'nginx_access_log': '/srv/logs/open-budgets_nginx_access.log',
    'nginx_error_log': '/srv/logs/open-budgets_nginx_error.log',
    'gunicorn_access_log': '/srv/logs/open-budgets_gunicorn_access.log',
    'gunicorn_error_log': '/srv/logs/open-budgets_gunicorn_error.log',
    'redis_access_log': '/srv/logs/open-budgets_redis_access.log',
    'redis_error_log': '/srv/logs/open-budgets_redis_error.log',
    'timestamp': datetime.datetime.now(),
}

WORKON = 'workon ' + CONFIG['project_name']

DEACTIVATE = 'deactivate'
