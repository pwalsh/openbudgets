import datetime
from fabric.api import env


env.use_ssh_config = True
env.forward_agent = True
env.user = 'openmuni'
env.roledefs = {
    'web': ['192.158.30.219']
}

KEY = env.user

MACHINE = {
    'LOCATION': env.roledefs['web'][0],
    'PORT': 80,
    'NAME': 'Open Muni Budgets',
    'OWNER_GROUP': 'www-data',
    'OWNER_USER': env.user,
    'OWNER_PROFILE': '/home/' + env.user + '/.profile',
    'DIR_USER_HOME': '/home/' + env.user,
    'DIR_MODE': 'g+s',
    'DIR_WORKSPACE': '/srv',
    'DIR_ENVIRONMENTS': '/srv/environments',
    'DIR_PROJECTS': '/srv/projects',
    'DIR_SSL': '/srv/ssl',
    'DIR_LOGS': '/srv/logs',
    'DATABASES': ['postgres', 'redis'],
    'ACTION_DATE': datetime.datetime.now()
}

PROJECT = {
    'APP_LOCATION': '127.0.0.1',
    'APP_PORT': 9999,
    'APP_WORKERS': 4,
    'APP_TIMEOUT': 45,
    'CELERY_CONCURRENCY': 1,
    'CELERY_MAX_TASKS_PER_CHILD': 10,
    'APP_WSGI': 'openbudget.wsgi:application',
    'NAME': MACHINE['NAME'],
    'DOMAINS': ['dev.openmuni.org.il', 'api.dev.openmuni.org.il',
                'en.dev.openmuni.org.il', 'he.dev.openmuni.org.il',
                'ar.dev.openmuni.org.il', 'ru.dev.openmuni.org.il'],
    'REPO': 'https://github.com/hasadna/omuni-budget',
    'BRANCH': 'develop',
    'ROOT': MACHINE['DIR_PROJECTS'] + '/' + KEY,
    'ENV': MACHINE['DIR_ENVIRONMENTS'] + '/' + KEY,
    'LOGS': {
        'NGINX_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_nginx_access.log',
        'NGINX_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_nginx_error.log',
        'GUNICORN_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_gunicorn_access.log',
        'GUNICORN_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_gunicorn_error.log',
        'CELERY': MACHINE['DIR_LOGS'] + '/' + KEY + '_celery.log',
        'REDIS_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_redis_access.log',
        'REDIS_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_redis_error.log',
    },
    'ACTION_DATE': datetime.datetime.now()
}
