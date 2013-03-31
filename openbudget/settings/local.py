from openbudget.settings.base import *


SESSION_COOKIE_DOMAIN = 'obudget.dev'

ADMINS = (
    ('', ''),
    ('', ''),
)

MANAGERS = ADMINS

MIDDLEWARE_CLASSES += (
    'openbudget.api.middleware.XsSharing',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

SENTRY_DSN = ''

INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEVSTRAP = {
    'FIXTURES': (
        'dev/sites',
        'demo/objects',
        'israel/strings'
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
