hosts = """### Generated via Fabric on ${ACTION_DATE}
# hosts configuration for ${NAME}
${LOCATION} ${KEY}
"""


profile = """### Generated via Fabric on ${ACTION_DATE}
# .profile configuration for ${NAME}
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export EDITOR=nano
export PYTHONIOENCODING=utf-8
export WORKON_HOME=${DIR_ENVIRONMENTS}
export PROJECT_HOME=${DIR_PROJECTS}
source /usr/local/bin/virtualenvwrapper.sh
export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
"""


nginx = """### Generated via Fabric on ${ACTION_DATE}
# nginx configuration for ${NAME}

upstream ${KEY} {
    server    ${APP_LOCATION}:${APP_PORT};
}

server {
    listen      *:${PORT};
    server_name ${SERVER_NAMES};
    root                 ${PROJECT_ROOT};
    access_log           ${ACCESS_LOG};
    error_log            ${ERROR_LOG};

    location /static/ {

    }

    location / {
        proxy_pass              http://${KEY};
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


gunicorn_supervisor = """; Generated via Fabric on ${ACTION_DATE}
; gunicorn configuration for ${NAME}
; usually would pass logs on gunicorn, but it errors:
; --access-logfile ${ACCESS_LOG} --error-logfile ${ERROR_LOG}

[program:${KEY}-gunicorn]

command=${PROJECT_ENV}/bin/gunicorn --bind ${APP_LOCATION}:${APP_PORT} --workers ${APP_WORKERS} ${APP_WSGI}

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


gunicorn_upstart = """### Generated via Fabric on ${ACTION_DATE}
# gunicorn configuration for ${NAME}

author "Paul Walsh"
description "Controls Gunicorn for ${NAME}"

start on runlevel [2345]
stop on runlevel [!2345]
respawn

env USER="${KEY}"
env ENVIRONMENT=${DIR_ENVIRONMENT}
env PROJECT=${DIR_PROJECT}
env LOGS=${DIR_LOGS}
env PYTHON=/bin/python
env MANAGE=/manage.py
env ACCESSLOG=${GUNICORN_ACCESS_LOG}
env ERRORLOG=${GUNICORN_ERROR_LOG}
env HOST=${APP_LOCATION}
env PORT=${APP_PORT}
env WORKERS=4

exec su -s /bin/sh -c 'exec "$0" "$@"' $USER -- $ENVIRONMENT$PYTHON $PROJECT$MANAGE run_gunicorn -b $HOST:$PORT -w $WORKERS --access-logfile $LOGS$ACCESSLOG --error-logfile $LOGS$ERRORLOG

"""


celery_upstart = """### Generated via Fabric on ${ACTION_DATE}
# celery configuration for ${NAME}

author "Paul Walsh"
description "Controls Celery for ${NAME}"

start on starting open-budget
stop on stopping open-budget
respawn

env USER="${USER}"
env ENVIRONMENT=${DIR_ENVIRONMENT}
env PROJECT=${DIR_PROJECT}
env LOGS=${DIR_LOGS}
env PYTHON=/bin/python
env MANAGE=/manage.py
env LOGFILE=${CELERY_LOG}
env CONCURRENCY=4
env MAX_TASKS_PER_CHILD=100
env BEATRECORD=/celerybeat-schedule.db

exec su -s /bin/sh -c 'exec "$0" "$@"' $USER -- $ENVIRONMENT$PYTHON $PROJECT$MANAGE celery worker --beat --schedule=$PROJECT$BEATRECORD --concurrency=$CONCURRENCY --maxtasksperchild=$MAX_TASKS_PER_CHILD --logfile=$LOGS$LOGFILE

"""

production_settings = """### Generated via Fabric on ${ACTION_DATE}
from openbudget.settings.base import *


DEBUG = False

TEMPLATE_DEBUG = DEBUG

MODELTRANSLATION_DEBUG = DEBUG

SECRET_KEY = '${SECRET_KEY}'

ALLOWED_HOSTS = ${ALLOWED_HOSTS}

SESSION_COOKIE_DOMAIN = '${SESSION_COOKIE_DOMAIN}'

EMAIL_HOST_USER = '${EMAIL_HOST_USER}'

EMAIL_HOST_PASSWORD = '${EMAIL_HOST_PASSWORD}'

ADMINS = ${ADMINS}

SENTRY_DSN = '${SENTRY_DSN}'

BROKER_URL = REDIS_URL

CELERY_RESULT_BACKEND = BROKER_URL

CELERY_RESULT_DBURI = ''

INTERNAL_IPS = ()

DEBUG_TOOLBAR_CONFIG = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${DATABASE_NAME}',
        'USER': '${DATABASE_USER}',
        'PASSWORD': '${PASSWORD}',
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
