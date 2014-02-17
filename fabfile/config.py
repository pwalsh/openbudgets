import datetime
from fabric.api import env
from fabric.contrib import django

PROJECT_NAME = 'openbudgets'
django.project(PROJECT_NAME)
from django.conf import settings

from fabfile import templates


LOCAL = {
    'roledefs': {'default': ['127.0.0.1'],
                 'app': ['127.0.0.1'],
                 'proxy': ['127.0.0.1'],
                 'cache': ['127.0.0.1'],
                 'queue': ['127.0.0.1'],
                 'db': ['127.0.0.1']},
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
    'db_dump_file': settings.OPENBUDGETS_TEMP_DIR + '/db_dump.sql',

    # email server
    'email_user': 'contact@openmuni.org.il',

    # code repository
    'repository_location': 'https://github.com/hasadna/openmuni-budgets',

    'dataset_root': settings.OPENBUDGETS_TEMP_DIR,
    'dataset_branch': 'master',
    'dataset_repository': 'https://github.com/prjts/openbudgets-data-israel',
    'storage_class': None,
    'dataset_processing_class': None,
}

STAGING_LOG_ROOT = '/srv/logs'
STAGING_ENVS = '/srv/environments'
STAGING_PROJECTS = '/srv/projects'
STAGING_PROJECT_DIR = '/openbudgets'

STAGING = {
    'email_host_user': 'hello@prjts.com',
    'roledefs': {'default': ['23.236.57.59'],
                 'app': ['23.236.57.59'],
                 'proxy': ['23.236.57.59'],
                 'cache': ['23.236.57.59'],
                 'queue': ['23.236.57.59'],
                 'db': ['108.59.81.226']},
    'app_wsgi': 'openbudgets.wsgi:application',
    'machine_location': '23.236.57.59',
    'machine_port': 80,
    'db_machine_location': '108.59.81.226',
    'db_private_network_location': '10.240.218.108',
    'db_machine_port': 5432,
    'initial_data': ['staging/sites'],
    'project_root': STAGING_PROJECTS + STAGING_PROJECT_DIR,
    'project_env': STAGING_ENVS + STAGING_PROJECT_DIR,
    'project_allowed_hosts': ['staging.openmuni.org.il'],
    'project_cookie_domain': 'openmuni.org.il',
    'target_settings_data': templates.deploy_settings,
    'target_settings_destination': STAGING_PROJECTS + STAGING_PROJECT_DIR + '/openbudgets/settings/deploy.py',
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
