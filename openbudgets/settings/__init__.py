import os


DEBUG = True

TEMPLATE_DEBUG = DEBUG

MODELTRANSLATION_DEBUG = DEBUG

WSGI_APPLICATION = 'openbudgets.wsgi.application'

SECRET_KEY = 'pvh9d)+7aui4=evh$yv!qgbr3oyz-4=^oj_%6g8+v57b=de5)7'

ALLOWED_HOSTS = ['.openbudgets.dev:8000']

SESSION_COOKIE_DOMAIN = 'openbudgets.dev'

SITE_ID = 1

TIME_ZONE = 'UTC'

USE_TZ = True

USE_I18N = True

USE_L10N = True

ROOT_URLCONF = 'openbudgets.urls'

SUBDOMAIN_URLCONFS = {
    '': 'openbudgets.urls',
    'www': 'openbudgets.urls',
    'he': 'openbudgets.urls',
    'en': 'openbudgets.urls',
    'ru': 'openbudgets.urls',
    'ar': 'openbudgets.urls',
    'api': 'openbudgets.urls',
}

gettext = lambda s: s
LANGUAGES = (
    ('he', gettext('Hebrew')),
    ('en', gettext('English')),
    ('ar', gettext('Arabic')),
    ('ru', gettext('Russian')),
)

LANGUAGE_CODE = LANGUAGES[0][0]

MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE

MODELTRANSLATION_FALLBACK_LANGUAGES = (LANGUAGES[0][0], LANGUAGES[1][0],
                                       LANGUAGES[2][0], LANGUAGES[3][0])

MEDIA_URL = '/static/media/'

STATIC_URL = '/static/'

SETTINGS_ROOT = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT = os.path.abspath(os.path.dirname(SETTINGS_ROOT))

MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(PROJECT_ROOT),
                                          'static', 'media'),)

STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(PROJECT_ROOT),
                                           'static'),)

STATICFILES_DIRS = (os.path.abspath(os.path.join(PROJECT_ROOT, 'commons',
                                                 'static')),)

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(PROJECT_ROOT, 'commons', 'templates')),
    # TODO: This below was added, check if it really should be here.
    os.path.abspath(os.path.join(PROJECT_ROOT, 'apps', 'entities', 'static', 'entities', 'explorer', 'templates')),
)

FIXTURE_DIRS = (os.path.abspath(os.path.join(PROJECT_ROOT, 'fixtures')),)

LOCALE_PATHS = (os.path.abspath(os.path.join(PROJECT_ROOT, 'locale')),)

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
    'django.middleware.locale.LocaleMiddleware',
    'openbudgets.apps.international.middleware.InterfaceLanguage',
    'django.middleware.common.CommonMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
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
    'grappelli.dashboard',
    'grappelli',
    'grappelli_modeltranslation',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'oauth2_provider',
    'corsheaders',
    'gunicorn',
    'south',
    'djcelery',
    'kombu.transport.django',
    'subdomains',
    'registration',
    'rest_framework',
    'modeltranslation',
    'taggit',
    'django_gravatar',
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
    'openbudgets.apps.api',
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
    'openbudgets.commons.context_processors.site',
    'openbudgets.commons.context_processors.forms',
    'openbudgets.commons.context_processors.openbudgets',
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
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

ACCOUNT_ACTIVATION_DAYS = 7

AUTH_USER_MODEL = 'accounts.Account'

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/accounts/auth/logout/'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/accounts/{uuid}/'.format(uuid=u.uuid)
}

GRAVATAR_DEFAULT_IMAGE = 'retro'

REDIS = {
    'HOST': '127.0.0.1',
    'PORT': 6379,
    'DB': 0,
    'PASSWORD': '',
    'SCHEME': 'redis://'
}

REDIS_URL = REDIS['SCHEME'] + REDIS['HOST'] + ':' + \
            str(REDIS['PORT']) + '/' + str(REDIS['DB'])

GRAPPELLI_ADMIN_TITLE = 'Open Budgets'


GRAPPELLI_INDEX_DASHBOARD = 'openbudget.dashboard.OpenBudgetsDashboard'

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

OAUTH2_PROVIDER = {
    'SCOPES': ['read', 'write']
}

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

import djcelery

djcelery.setup_loader()

BROKER_URL = 'django://'

CELERY_RESULT_BACKEND = 'database'

CELERY_RESULT_DBURI = os.path.abspath(os.path.join(
    os.path.dirname(PROJECT_ROOT), 'celery.db'))

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

SENTRY_DSN = ''

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CACHE_MIDDLEWARE_SECONDS = 604800

CACHE_MIDDLEWARE_KEY_PREFIX = 'openbudgets::'

SOUTH_TESTS_MIGRATE = False

OPENBUDGETS_TEMP_DIR = os.path.abspath(
    os.path.join(os.path.dirname(PROJECT_ROOT), 'tmp'))

OPENBUDGETS_NAME_APP = gettext('Open Local Budgets')

OPENBUDGETS_NAME_SPONSOR = gettext('Public Knowledge Workshop')

OPENBUDGETS_GROUP_ID_CORE = 1

OPENBUDGETS_GROUP_ID_CONTENT = 2

OPENBUDGETS_GROUP_ID_PUBLIC = 3

OPENBUDGETS_PERIOD_RANGES = ('yearly',)

OPENBUDGETS_AVATAR_ANON = STATIC_URL + 'img/avatar_anon.png'

OPENBUDGETS_IMPORT_FIELD_DELIMITER = ','

OPENBUDGETS_IMPORT_INTRA_FIELD_DELIMITER = '|'

OPENBUDGETS_IMPORT_INTRA_FIELD_MULTIPLE_VALUE_DELIMITER = ';'

OPENBUDGETS_COMPARABLE_TEMPLATENODE__DEFAULT = True

OPENBUDGETS_COMPARABLE_TEMPLATENODE_NOT_IN_BLUEPRINT_DEFAULT = True

OPENBUDGETS_COMPARABLE_WITHIN_ENTITY = True

OPENBUDGETS_COMPARABLE_ACROSS_ENTITIES = True

OPENBUDGETS_CKAN = [
    {
        'name': 'Datahub',
        'base_url': 'http://datahub.io/api',
        'package_url': 'http://datahub.io/dataset/',
        'api_key': '884da76c-87b6-4974-97dc-cfd3f639d15a'
    }
]

OPENBUDGETS_SETTING = {
    'tags': ['budget', 'municipalities', 'israel'],
    'notes': 'This is the Budget and the Actual of',
    'owner_org': 'israel-municipalities'
}

IMPORT_PRIORITY = ['slug',
                    'name',
                    'id'
]

IMPORT_SEPARATOR = ':'


# if we are on staging, we should have a settings.staging module to load.
try:
    from .staging import *
except ImportError:
    # if we are on local, we accept overrides in a settings.local module.
    # For safety, we only try to load settings.local if settings.production
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
