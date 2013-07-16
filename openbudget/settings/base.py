import os

DEBUG = False

TEMPLATE_DEBUG = DEBUG

MODELTRANSLATION_DEBUG = DEBUG

SECRET_KEY = 'pvh9d)+7aui4=evh$yv!qgbr3oyz-4=^oj_%6g8+v57b=de5)7'

ALLOWED_HOSTS = ['.open-budget.prjts.com']

SESSION_COOKIE_DOMAIN = 'open-budget.prjts.com'

SETTINGS_ROOT = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT = os.path.abspath(os.path.dirname(SETTINGS_ROOT))

WSGI_APPLICATION = 'openbudget.wsgi.application'

SITE_ID = 1

TIME_ZONE = 'UTC'

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openbudget',
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

MEDIA_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(PROJECT_ROOT),
        'static',
        'media'
    )
)

MEDIA_URL = '/static/media/'

STATIC_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(PROJECT_ROOT),
        'static'
    )
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.abspath(
        os.path.join(PROJECT_ROOT, 'commons', 'static')
    ),
)

TEMPLATE_DIRS = (
    os.path.abspath(
        os.path.join(PROJECT_ROOT, 'commons', 'templates')
    ),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'openbudget.apps.international.middleware.InterfaceLanguage',
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
    'haystack',
    'djcelery',
    'subdomains',
    'registration',
    'rest_framework',
    'modeltranslation',
    'taggit',
    'openbudget.apps.accounts',
    'openbudget.apps.sheets',
    'openbudget.apps.contexts',
    'openbudget.apps.entities',
    'openbudget.apps.interactions',
    'openbudget.apps.international',
    'openbudget.apps.pages',
    'openbudget.apps.sources',
    'openbudget.apps.taxonomies',
    'openbudget.apps.transport',
    'openbudget.apps.projects',
    'openbudget.api',
    'openbudget.commons',
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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'openbudget.commons.context_processors.get_site',
)

# FIXTURE CONF
FIXTURE_DIRS = (
    os.path.abspath(os.path.join(PROJECT_ROOT, 'fixtures')),
)

# URL CONF
ROOT_URLCONF = 'openbudget.ui.urls'

SUBDOMAIN_URLCONFS = {
    '': 'openbudget.ui.urls',
    'www': 'openbudget.ui.urls',
    'he': 'openbudget.ui.urls',
    'en': 'openbudget.ui.urls',
    'ru': 'openbudget.ui.urls',
    'ar': 'openbudget.ui.urls',
    'api': 'openbudget.api.urls',
}

# INTERNATIONALIZATION CONF
USE_I18N = True

USE_L10N = True

LOCALE_PATHS = (
    os.path.abspath(os.path.join(PROJECT_ROOT, 'locale')),
)

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

# UNICODE SLUG CONF
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# USER ACCOUNT CONF
ACCOUNT_ACTIVATION_DAYS = 7

AUTH_USER_MODEL = 'accounts.Account'

LOGIN_URL = '/accounts/auth/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/accounts/auth/logout/'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/accounts/{uuid}/'.format(uuid=u.uuid)
}

# CACHE CONF
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

CACHE_MIDDLEWARE_SECONDS = 600

CACHE_MIDDLEWARE_KEY_PREFIX = 'omuni'

# GRAPPELLI CONF
GRAPPELLI_ADMIN_TITLE = 'Open Budget'

GRAPPELLI_INDEX_DASHBOARD = 'openbudget.dashboard.OpenBudgetDashboard'

# DJANGO REST FRAMEWORK CONF
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

# OAUTH2 PROVIDER CONF
OAUTH2_PROVIDER = {
    'SCOPES': ['read', 'write']
}

# DJANGO CORS HEADERS CONF
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    #'DELETE',
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

# CORS_ALLOW_CREDENTIALS = False

# HAYSTACK CONF
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'commons', 'search', 'index'),
    },
}

# CELERY CONF
import djcelery

djcelery.setup_loader()

BROKER_URL = REDIS['SCHEME'] + REDIS['HOST'] + ':' + str(REDIS['PORT']) + '/' + \
             str(REDIS['DB'])

CELERY_RESULT_BACKEND = BROKER_URL

# EMAIL CONF
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

# SENTRY CONF
SENTRY_DSN = ''

# DEVELOPER ADMINS CONF
ADMINS = (
    ('', ''),
    ('', ''),
)

# OPEN BUDGET CUSTOM CONF
TEMP_FILES_DIR = os.path.abspath(os.path.join(os.path.dirname(PROJECT_ROOT), 'tmp'))

OPENBUDGET_CORE_TEAM_ID = 1

OPENBUDGET_CONTENT_TEAM_ID = 2

OPENBUDGET_PUBLIC_ID = 3

OPENBUDGET_PERIOD_RANGES = ('yearly',)
