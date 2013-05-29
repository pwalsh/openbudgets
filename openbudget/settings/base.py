import os

DEBUG = False

TEMPLATE_DEBUG = DEBUG

MODELTRANSLATION_DEBUG = DEBUG

SECRET_KEY = 'pvh9d)+7aui4=evh$yv!qgbr3oyz-4=^oj_%6g8+v57b=de5)7'

SETTINGS_ROOT = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT = os.path.abspath(os.path.dirname(SETTINGS_ROOT))

WSGI_APPLICATION = 'openbudget.wsgi.application'

SITE_ID = 1

TIME_ZONE = 'UTC'

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(os.path.dirname(PROJECT_ROOT), 'local.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
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
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'openbudget.apps.international.middleware.InterfaceLanguage',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
    'gunicorn',
    'south',
    'haystack',
    'djcelery',
    'subdomains',
    'registration',
    'rest_framework',
    'provider',
    'provider.oauth2',
    'rosetta_grappelli',
    'rosetta',
    'modeltranslation',
    'taggit',
    'openbudget.apps.accounts',
    'openbudget.apps.budgets',
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

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/accounts/logout/'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/accounts/{uuid}/'.format(uuid=u.uuid)
}

# GRAPPELLI CONF
GRAPPELLI_ADMIN_TITLE = 'Open Budget'

GRAPPELLI_INDEX_DASHBOARD = 'openbudget.dashboard.OpenBudgetDashboard'

# DJANGO REST FRAMEWORK CONF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'PAGINATE_BY': 50
}

# OAUTH2 PROVIDER CONF
OAUTH_ENFORCE_SECURE = True

# HAYSTACK CONF
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'commons', 'search', 'index'),
    },
}

# CELERY CONF
from celery.schedules import crontab
import djcelery

djcelery.setup_loader()

BROKER_URL = 'redis://127.0.0.1:6379/'

CELERYBEAT_SCHEDULE = {
    "update_index": {
        "task": "tasks.update_index",
        "schedule": crontab(
           minute=0,
            hour=0
        ),
    },
    "rebuild_index": {
        "task": "tasks.rebuild_index",
        "schedule": crontab(
            day_of_week='saturday',
            minute=0,
            hour=0
        ),
    }
}

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
