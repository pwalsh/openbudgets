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

CACHEOPS = {
    'django.contrib.sites.*': ('all', OPENBUDGETS_QUERYSET_CACHE_EXPIRY),
    'contexts.*': ('all', OPENBUDGETS_QUERYSET_CACHE_EXPIRY),
    'entities.*': ('all', OPENBUDGETS_QUERYSET_CACHE_EXPIRY),
    'sheets.*': ('all', OPENBUDGETS_QUERYSET_CACHE_EXPIRY),
}

EMAIL_HOST_USER = '${email_user}'
EMAIL_HOST_PASSWORD = '${email_password}'
ADMINS = ${project_admins}

OPENBUDGETS_COMPARABLE_NODE_DEFAULT = ${openbudgets_comparable_node_default}
OPENBUDGETS_COMPARABLE_NODE_IN_BLUEPRINT = ${openbudgets_comparable_node_in_blueprint}
OPENBUDGETS_COMPARABLE_NODE_NOT_IN_BLUEPRINT = ${openbudgets_comparable_node_not_in_blueprint}
OPENBUDGETS_COMPARABLE_OVERRIDE_BY_INHERITANCE = ${openbudgets_comparable_override_by_inheritance}
OPENBUDGETS_COMPARABLE_STRICT_BY_DECLARATION = ${openbudgets_comparable_strict_by_declaration}
OPENBUDGETS_COMPARABLE_WITHIN_ENTITY = ${openbudgets_comparable_within_entity}
OPENBUDGETS_COMPARABLE_ACROSS_ENTITIES = ${openbudgets_comparable_across_entities}
OPENBUDGETS_COMPARABLE_NEVER_DISPLAY_NON_COMPARABLE = ${openbudgets_comparable_never_display_non_comparable}

OPENBUDGETS_UI['enable'] = ${openbudgets_ui_enable}
OPENBUDGETS_API['enable'] = ${openbudgets_api_enable}
OPENBUDGETS_ADMIN['enable'] = ${openbudgets_admin_enable}

OPENBUDGETS_CONSOLE_QUERY_DEBUG = ${openbudgets_console_query_debug}

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
