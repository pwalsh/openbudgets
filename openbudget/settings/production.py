from openbudget.settings.base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = '!2k4w$5xwlir)r93(-2t^am!l62qd=is3(sgo$t9imff0(mbs*'

SESSION_COOKIE_DOMAIN = 'open-budget.prjts.com'
ALLOWED_HOSTS = ['.open-budget.prjts.com']

ADMINS = (
    ('', ''),
    ('', ''),
)

MANAGERS = ADMINS

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

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

SENTRY_DSN = ''
