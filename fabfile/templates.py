deploy = """### Generated via Fabric on ${timestamp}
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

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '${cache_private_network_location}' + ':' + str(REDIS['PORT']),
        'OPTIONS': {
            'DB': REDIS['DB'],
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

EMAIL_HOST_USER = '${email_host_user}'

EMAIL_HOST_PASSWORD = '${email_host_password}'

ADMINS = (('Paul Walsh', 'paulywalsh@gmail.com'),
          ('Ido Ivri', 'idoivri@gmail.com'),)


"""
