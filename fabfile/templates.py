deploy = """### Generated via Fabric on ${timestamp}
from ${project_name}.settings import *

DEBUG = False

ALLOWED_HOSTS = ${project_allowed_hosts}
SESSION_COOKIE_DOMAIN = '${project_cookie_domain}'

RAVEN_CONFIG['dsn'] = '${sentry_dsn}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': '${db_user}',
        'PASSWORD': '${db_password}',
        'HOST': '${db_location}',
        'PORT': '${db_port}',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}

EMAIL_HOST_USER = '${email_user}'
EMAIL_HOST_PASSWORD = '${email_password}'
ADMINS = ${project_admins}

OPENBUDGETS_UI['enable'] = ${openbudgets_ui_enable}
OPENBUDGETS_API['enable'] = ${openbudgets_api_enable}
OPENBUDGETS_ADMIN['enable'] = ${openbudgets_admin_enable}

"""


local = """from openbudgets.settings import *

EMAIL_HOST_USER = '${email_user}'
EMAIL_HOST_PASSWORD = '${email_password}'
ADMINS = (('', ''),)

# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS += ('debug_toolbar',)
# INTERNAL_IPS = ('127.0.0.1',)
# DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

# CACHES = {
#    'default': {
#        'BACKEND': 'redis_cache.RedisCache',
#        'LOCATION': REDIS['HOST'] + ':' + str(REDIS['PORT']),
#        'OPTIONS': {
#            'DB': REDIS['DB'],
#            'PARSER_CLASS': 'redis.connection.HiredisParser'
#        },
#    },
# }
#
# BROKER_URL = REDIS_URL
#
# CELERY_RESULT_BACKEND = BROKER_URL
#
# CELERY_RESULT_DBURI = ''
"""
