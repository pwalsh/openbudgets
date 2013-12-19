import datetime
from fabric.api import env
from fabric.contrib import django

PROJECT_NAME = 'openbudgets'
django.project(PROJECT_NAME)
from django.conf import settings

from fabfile import templates


LOCAL = {

    'django_settings': settings,
    'project_name': PROJECT_NAME,
    'project_root': settings.PROJECT_ROOT,
    'initial_data': ['local/sites'],
    'project_allowed_hosts': [''],
    'project_cookie_domain': '',
    'secret_key': '',

    'app_wsgi': '',

    # virtualenv
    'workon': 'workon openbudgets',
    'deactivate': 'deactivate',

    # db server
    'db_name': 'openbudgets',
    'db_user': 'robot',
    'db_dump_file': settings.OPENBUDGETS_TEMP_DIR + '/dump_{timestamp}.sql'.format(timestamp=datetime.datetime.now()),

    # email server
    'email_user': 'contact@openmuni.org.il',

    # code repository
    'repository_location': 'https://github.com/hasadna/openmuni-budgets',

    'dataset_root': settings.OPENBUDGETS_TEMP_DIR,
    'dataset_branch': 'master',
    'dataset_repository': 'https://github.com/prjts/openbudgets-data-israel',

}

STAGING_LOG_ROOT = '/srv/logs'
STAGING_ENVS = '/srv/environments'
STAGING_PROJECTS = '/srv/projects'
STAGING_PROJECT_DIR = '/openbudgets'

STAGING = {
    'email_host_user': 'hello@prjts.com',
    'roledefs': {'default': ['162.243.66.200'],
                 'app': ['162.243.66.200'],
                 'proxy': ['162.243.66.200'],
                 'cache': ['162.243.66.200'],
                 'queue': ['162.243.66.200'],
                 'db': ['162.243.85.165']},
    'app_wsgi': 'openbudgets.wsgi:application',
    'machine_location': '162.243.66.200',
    'machine_port': 80,
    'db_machine_location': '162.243.85.165',
    'db_private_network_location': '10.128.29.136',
    'db_machine_port': 5432,
    'initial_data': ['staging/sites'],
    'project_root': STAGING_PROJECTS + STAGING_PROJECT_DIR,
    'project_env': STAGING_ENVS + STAGING_PROJECT_DIR,
    'project_allowed_hosts': ['staging.openmuni.org.il'],
    'project_cookie_domain': 'openmuni.org.il',
    'target_settings_data': templates.staging_settings,
    'target_settings_destination': STAGING_PROJECTS + STAGING_PROJECT_DIR + '/openbudgets/settings/staging.py',
    'log_proxy_access': STAGING_LOG_ROOT + '/proxy_access.log',
    'log_proxy_error': STAGING_LOG_ROOT + '/proxy_error.log',
    'log_app_access': STAGING_LOG_ROOT + '/app_access.log',
    'log_app_error': STAGING_LOG_ROOT + '/app_access.log',
    'log_queue_access': STAGING_LOG_ROOT + '/queue_access.log',
    'log_cache_access': STAGING_LOG_ROOT + '/cache_access.log',
    'log_cache_error': STAGING_LOG_ROOT + '/cache_error.log',
}

# The default environment is LOCAL
env.update(LOCAL)
