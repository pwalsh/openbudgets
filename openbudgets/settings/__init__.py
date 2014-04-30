import os


WSGI_APPLICATION = 'openbudgets.wsgi.application'

SECRET_KEY = 'pvh9d)+7aui4=evh$yv!qgbr3oyz-4=^oj_%6g8+v57b=de5)7'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.openbudgets.dev:8000']
SESSION_COOKIE_DOMAIN = 'openbudgets.dev'

TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True

SITE_ID = 1
ROOT_URLCONF = 'openbudgets.urls'
SUBDOMAIN_URLCONFS = {
    None: ROOT_URLCONF,
    'www': ROOT_URLCONF,
    'he': ROOT_URLCONF,
    'en': ROOT_URLCONF,
    'ru': ROOT_URLCONF,
    'ar': ROOT_URLCONF,
}

gettext = lambda s: s
LANGUAGES = (
    ('he', gettext('Hebrew')),
    ('en', gettext('English')),
    ('ar', gettext('Arabic')),
    ('ru', gettext('Russian')),
)
LANGUAGE_CODE = LANGUAGES[0][0]

STATIC_URL = '/static/'
MEDIA_URL = '/static/media/'

SETTINGS_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(SETTINGS_ROOT))
REPOSITORY_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))
STATIC_ROOT = os.path.abspath(os.path.join(REPOSITORY_ROOT, 'static'),)
MEDIA_ROOT = os.path.abspath(os.path.join(STATIC_ROOT, 'media'),)
LOCALE_PATHS = (os.path.abspath(os.path.join(PROJECT_ROOT, 'locale')),)
STATICFILES_DIRS = (os.path.abspath(os.path.join(PROJECT_ROOT, 'commons', 'static')),)
FIXTURE_DIRS = (os.path.abspath(os.path.join(PROJECT_ROOT, 'fixtures')),)
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(PROJECT_ROOT, 'commons', 'templates')),
    os.path.abspath(os.path.join(PROJECT_ROOT, 'apps', 'entities', 'static', 'entities', 'explorer', 'templates')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'openbudgets.commons.stache.PystacheFilesystemLoader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'openbudgets.apps.international.middleware.InterfaceLanguage',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'cacheops',
    'corsheaders',
    'django_gravatar',
    'oauth2_provider',
    'raven.contrib.django.raven_compat',
    'registration',
    'rest_framework',
    'south',
    'subdomains',
    'taggit',
    'openbudgets.apps.accounts',
    'openbudgets.apps.sheets',
    'openbudgets.apps.contexts',
    'openbudgets.apps.entities',
    'openbudgets.apps.interactions',
    'openbudgets.apps.international',
    'openbudgets.apps.pages',
    'openbudgets.apps.sources',
    'openbudgets.apps.taxonomies',
    'openbudgets.apps.tools',
    'openbudgets.apps.transport',
    'openbudgets.api',
    'openbudgets.ui',
    'openbudgets.commons',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'openbudgets.commons.context_processors.forms',
    'openbudgets.commons.context_processors.openbudgets',
    'openbudgets.commons.context_processors.site',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

SOUTH_TESTS_MIGRATE = False
SOUTH_MIGRATION_MODULES = {'taggit': 'taggit.south_migrations'}

RAVEN_CONFIG = {'dsn': ''}

ACCOUNT_ACTIVATION_DAYS = 7
AUTH_USER_MODEL = 'accounts.Account'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/accounts/auth/logout/'
ABSOLUTE_URL_OVERRIDES = {'auth.user': lambda u: '/accounts/{uuid}/'.format(uuid=u.uuid)}
GRAVATAR_DEFAULT_IMAGE = 'retro'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        #'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        #'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.UnicodeJSONRenderer',
        #'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'PAGINATE_BY': 500,
    'PAGINATE_BY_PARAM': 'page_by'
}

OAUTH2_PROVIDER = {'SCOPES': ['read', 'write']}
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS')
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

ADMINS = (('', ''),)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openbudgets',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}

REDIS = {
    'HOST': '127.0.0.1',
    'PORT': 6379,
    'DB': 0,
    'PASSWORD': '',
    'SCHEME': 'redis://'
}

REDIS_URL = REDIS['SCHEME'] + REDIS['HOST'] + ':' +\
            str(REDIS['PORT']) + '/' + str(REDIS['DB'])

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'KEY_PREFIX': 'openbudgets::',
        'VERSION': 1,
        'TIMEOUT': 5000,
        'MAX_ENTRIES': 3000,
        'OPTIONS': {},
    },
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_KEY_PREFIX = CACHES['default']['KEY_PREFIX']
CACHE_MIDDLEWARE_SECONDS = 604800

OPENBUDGETS_QUERYSET_CACHE_EXPIRY = 60*60*24*30  # 30 days

CACHEOPS_REDIS = {
    'host': REDIS['HOST'],
    'port': REDIS['PORT'],
    'db': REDIS['DB'],
    'socket_timeout': 3,
}

CACHEOPS = {
    'django.contrib.sites.*': ('all', OPENBUDGETS_QUERYSET_CACHE_EXPIRY),
    'contexts.*': ('all', OPENBUDGETS_QUERYSET_CACHE_EXPIRY),
    'entities.*': ('all', OPENBUDGETS_QUERYSET_CACHE_EXPIRY),
    'sheets.*': ('all', OPENBUDGETS_QUERYSET_CACHE_EXPIRY),
}

OPENBUDGETS_TEMP_DIR = os.path.abspath(os.path.join(REPOSITORY_ROOT, 'tmp'))

OPENBUDGETS_NAME_APP = gettext('Open Local Budgets')
OPENBUDGETS_NAME_SPONSOR = gettext('Public Knowledge Workshop')

OPENBUDGETS_GROUP_ID_CORE = 1
OPENBUDGETS_GROUP_ID_CONTENT = 2
OPENBUDGETS_GROUP_ID_PUBLIC = 3

OPENBUDGETS_AVATAR_ANON = STATIC_URL + 'img/avatar_anon.png'

OPENBUDGETS_IMPORT_FIELD_DELIMITER = ','
OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER = '|'
OPENBUDGETS_IMPORT_INTRA_FIELD_MULTIPLE_VALUE_DELIMITER = ';'

OPENBUDGETS_COMPARABLE_NODE_DEFAULT = False
OPENBUDGETS_COMPARABLE_NODE_IN_BLUEPRINT = False
OPENBUDGETS_COMPARABLE_NODE_NOT_IN_BLUEPRINT = False
OPENBUDGETS_COMPARABLE_OVERRIDE_BY_INHERITANCE = False
OPENBUDGETS_COMPARABLE_STRICT_BY_DECLARATION = True
OPENBUDGETS_COMPARABLE_WITHIN_ENTITY = True
OPENBUDGETS_COMPARABLE_ACROSS_ENTITIES = True

OPENBUDGETS_PERIOD_RANGES = ('yearly',)

OPENBUDGETS_CKAN_BACKENDS = [
    {
        'name': 'DataHub',
        'base_url': 'http://datahub.io/api',
        'package_url': 'http://datahub.io/dataset/',
        'api_key': '884da76c-87b6-4974-97dc-cfd3f639d15a'
    }
]

OPENBUDGETS_CKAN_CONFIG = {
    'tags': ['budget', 'municipalities', 'israel'],
    'notes': 'This is the Budget and the Actual of',
    'owner_org': 'israel-municipalities'
}

OPENBUDGETS_UI = {
    'enable': False,
    'base': ''
}

OPENBUDGETS_API = {
    'enable': True,
    'base': 'api/',
    'base_without_ui': ''
}

OPENBUDGETS_ADMIN = {
    'enable': False,
    'base': 'admin/'
}

OPENBUDGETS_CONSOLE_QUERY_DEBUG = False


# if we are on a deploy env, we should have a settings.deploy module to load.
try:
    from .deploy import *
except ImportError:
    # if we are on local, we accept overrides in a settings.local module.
    # For safety, we only try to load settings.local if settings.deploy
    # does not exist.
    try:
        from .local import *
    except ImportError:
        pass


# if we are on the CI server, load some CI-specific settings
try:
    ci = os.environ.get('CI')
    if ci:
        from .ci import *
except KeyError:
    pass
