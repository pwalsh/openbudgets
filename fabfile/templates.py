staging_settings = """### Generated via Fabric on ${timestamp}
from ${project_name}.settings import *


ALLOWED_HOSTS = ${project_allowed_hosts}

SESSION_COOKIE_DOMAIN = '${project_cookie_domain}'

SENTRY_DSN = '${sentry_dsn}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': '${db_user}',
        'PASSWORD': '${db_password}',
        'HOST': '${db_machine_location}',
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
