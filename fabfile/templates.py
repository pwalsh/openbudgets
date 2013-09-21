nginx = """### Generated via Fabric on ${timestamp}
# nginx configuration for ${project_name}

upstream ${project_name} {
    server    ${app_location}:${app_port};
}

server {
    listen      *:${machine_port};
    server_name ${domain_names};
    root                 ${project_root};
    access_log           ${nginx_access_log};
    error_log            ${nginx_error_log};

    location /static/ {

    }

    location / {
        proxy_pass              http://${project_name};
        proxy_redirect          off;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        client_max_body_size    10m;
        client_body_buffer_size 128k;
        proxy_connect_timeout   90;
        proxy_send_timeout      90;
        proxy_read_timeout      90;
        proxy_buffers           32 4k;
    }
}
"""


production_settings = """### Generated via Fabric on ${timestamp}
from slatemath.settings import *

DEBUG = False

TEMPLATE_DEBUG = DEBUG

MODELTRANSLATION_DEBUG = DEBUG

SECRET_KEY = '${secret_key}'

ALLOWED_HOSTS = ${allowed_hosts}

SESSION_COOKIE_DOMAIN = '${cookie_domain}'

SENTRY_DSN = '${sentry_dsn}'

EMAIL_HOST_USER = '${email_user}'

EMAIL_HOST_PASSWORD = '${email_password}'

ADMINS = ${ADMINS}

BROKER_URL = REDIS_URL

CELERY_RESULT_BACKEND = BROKER_URL

CELERY_RESULT_DBURI = ''

INTERNAL_IPS = ()

DEBUG_TOOLBAR_CONFIG = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': '${db_user}',
        'PASSWORD': '${password}',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': REDIS['HOST'] + ':' + str(REDIS['PORT']),
        'OPTIONS': {
            'DB': REDIS['DB'],
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}
"""


gunicorn_supervisor = """; Generated via Fabric on ${ACTION_DATE}
; gunicorn configuration for ${NAME}
; usually would pass logs on gunicorn, but it errors:
; --access-logfile ${ACCESS_LOG} --error-logfile ${ERROR_LOG}

[program:${KEY}-gunicorn]

command=${PROJECT_ENV}/bin/gunicorn --bind ${APP_LOCATION}:${APP_PORT} --timeout ${APP_TIMEOUT} --workers ${APP_WORKERS} ${APP_WSGI}

environment=PATH="${PROJECT_ENV}/bin"
directory=${PROJECT_ROOT}
user=${KEY}
redirect_stderr=true
autostart=true
autorestart=true
"""


celery_supervisor = """### Generated via Fabric on ${ACTION_DATE}
# celery configuration for ${NAME}
[program:${KEY}-celery]

command=${PROJECT_ENV}/bin/python manage.py celery worker --concurrency=${CONCURRENCY} --maxtasksperchild=${MAX_TASKS_PER_CHILD} --logfile=${ACCESS_LOG}

environment=PATH="${PROJECT_ENV}/bin"
directory=${PROJECT_ROOT}
user=${KEY}
redirect_stderr=true
autostart=true
autorestart=true
"""


gunicorn_upstart = """### Generated via Fabric on ${timestamp}
# gunicorn upstart configuration for ${project_name}

author "Paul Walsh"
description "Controls Gunicorn for ${project_name}"

start on (filesystem)
stop on runlevel [016]
respawn
console log
setuid ${user}
setgid ${user}
chdir ${project_root}

exec ${project_env}/bin/gunicorn ${app_wsgi} --bind ${app_location}:${app_port} --workers ${app_workers} --timeout ${app_timeout} --access-logfile ${gunicorn_access_log} --error-logfile ${gunicorn_error_log}
"""


celery_upstart = """### Generated via Fabric on ${ACTION_DATE}
# celery configuration for ${NAME}

author "Paul Walsh"
description "Controls Celery for ${NAME}"

start on starting open-budget
stop on stopping open-budget
respawn

"""
