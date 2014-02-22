deploy_settings = """### Generated via Fabric on ${timestamp}
from ${project_name}.settings import *


ALLOWED_HOSTS = ${project_allowed_hosts}

SESSION_COOKIE_DOMAIN = '${project_cookie_domain}'

RAVEN_CONFIG['dsn'] = '${sentry_dsn}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': '${db_user}',
        'PASSWORD': '${db_password}',
        'HOST': '${db_private_network_location}',
        'PORT': '${db_machine_port}',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}

EMAIL_HOST_USER = '${email_host_user}'

EMAIL_HOST_PASSWORD = '${email_host_password}'

ADMINS = (('Paul Walsh', 'paulywalsh@gmail.com'),
          ('Ido Ivri', 'idoivri@gmail.com'),)


"""


circus = """### Generated via Fabric on ${timestamp}
[watcher:openbudgets-app]
cmd = /srv/environments/openbudgets/bin/chaussette --fd $(circus.sockets.openbudgets-app) --backend meinheld openbudgets.wsgi:application
numprocesses = 4
use_sockets = True

[socket:openbudgets-app]
host = 127.0.0.1
port = 9000

"""
