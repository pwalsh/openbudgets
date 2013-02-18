import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Paul Walsh', 'paulywalsh@gmail.com'),
    ('Yehonatan Daniv', 'maggotfish@gmail.com'),
)

MANAGERS = ADMINS

# will be updated for deployment
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

TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.abspath(
    os.path.join(PROJECT_ROOT, 'static', 'media')
)

MEDIA_URL = '/static/media/'

STATIC_ROOT = os.path.abspath(
    os.path.join(PROJECT_ROOT, 'static')
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.abspath(
        os.path.join(PROJECT_ROOT, 'commons', 'static')
    ),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'pvh9d)+7aui4=evh$yv!qgbr3oyz-4=^oj_%6g8+v57b=de5)7'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'omuni.commons.middleware.InterfaceLanguage',
    'django.middleware.common.CommonMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # debug_toolbar for development only
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'omuni.urls'

SUBDOMAIN_URLCONFS = {
    None: 'omuni.urls',
    'www': 'omuni.urls',
    'he': 'omuni.urls',
    'en': 'omuni.urls',
    'ru': 'omuni.urls',
    'ar': 'omuni.urls',
    'api': 'omuni.api.urls',
}

WSGI_APPLICATION = 'omuni.wsgi.application'

TEMPLATE_DIRS = (
    os.path.abspath(
        os.path.join(PROJECT_ROOT, 'commons', 'templates')
    ),
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
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'south',
    'subdomains',
    'registration',
    'rest_framework',
    'rosetta_grappelli',
    'rosetta',
    'modeltranslation',
    'omuni.accounts',
    'omuni.api',
    'omuni.budgets',
    'omuni.commons',
    'omuni.govts',
    'omuni.interactions',
    'omuni.pages',

    # debug_toolbar for development only
    'debug_toolbar',

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
    # here are the django defaults
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # and here our additions for the project
    'django.core.context_processors.request',
    'omuni.commons.context_processors.get_site',
)

FIXTURE_DIRS = (
    os.path.abspath(
        os.path.join(PROJECT_ROOT, 'fixtures')
    ),
)

# Supported languages
gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('he', gettext('Hebrew')),
    ('ar', gettext('Arabic')),
    ('ru', gettext('Russian')),
)

# We do unicode slugs around here, not transliterations...
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

ACCOUNT_ACTIVATION_DAYS = 7

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/accounts/logout/'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/accounts/%s/" % u.get_profile.uuid,
}

# SMTP configuration
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

# Grappelli configuration
GRAPPELLI_ADMIN_TITLE = 'Open Budget'

GRAPPELLI_INDEX_DASHBOARD = 'omuni.dashboard.OpenBudgetDashboard'

# Django REST Framework configuration
REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    'PAGINATE_BY': 10

}

# Comments
COMMENTS_APP = 'omuni.interactions'
COMMENTS_HIDE_REMOVED = True
COMMENT_MAX_LENGTH = 10000

# Sessions apply for all subdomains
# CHANGE FOR settings_local
#SESSION_COOKIE_DOMAIN='obudget.org.il'
SESSION_COOKIE_DOMAIN='obudget.dev'

# MOVE ANYTHING BELOW TO: settings_local.py

# debug_toolbar stuff
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
