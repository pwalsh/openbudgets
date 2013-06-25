from openbudget.settings.base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

MODELTRANSLATION_DEBUG = DEBUG

SESSION_COOKIE_DOMAIN = 'obudget.dev'

ADMINS = (
    ('Paul Walsh', 'paulywalsh@gmail.com'),
    #('', ''),
)

MANAGERS = ADMINS

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.abspath(os.path.join(os.path.dirname(PROJECT_ROOT), 'local.db')),
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'omuni',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '',
    }
}

MIDDLEWARE_CLASSES = (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'openbudget.apps.international.middleware.InterfaceLanguage',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'openbudget.api.middleware.XsSharing',
)


MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_pdb.middleware.PdbMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
    'django_pdb',
)

# CACHE CONF - Uncomment to disable caching in development
CACHES = {
   'default': {
       'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
   }
}

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

OAUTH_ENFORCE_SECURE = False

SENTRY_DSN = ''


INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEVSTRAP = {
    'FIXTURES': (
        'dev/sites',
        'locale/he/strings',
        'dev/interactions',
        'dev/sources',
        'dev/projects'
    ),
    'TESTS': (
        'accounts',
        'api',
        'sheets',
        'commons',
        'contexts',
        'entities',
        'interactions',
        'international',
        'pages',
        'sources',
        'taxonomies',
        'transport'
    )
}
