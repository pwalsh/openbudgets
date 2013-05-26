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

MIDDLEWARE_CLASSES += (
    'openbudget.api.middleware.XsSharing',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_pdb.middleware.PdbMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
    'django_pdb',
)

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'hello@prjts.com'

EMAIL_HOST_PASSWORD = 'wer74qPAL'

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
        'dev/sources'
    ),
    'TESTS': (
        'accounts',
        'api',
        'budgets',
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
