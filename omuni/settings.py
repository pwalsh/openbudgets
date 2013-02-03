import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Paul Walsh', 'paulywalsh@gmail.com'),
    ('Yehonatan Daniv', 'maggotfish@gmail.com'),
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

TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'static', 'media'))

MEDIA_URL = '/static/media/'

STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'static'))

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.abspath(os.path.join(PROJECT_ROOT, 'commons', 'static')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'pvh9d)+7aui4=evh$yv!qgbr3oyz-4=^oj_%6g8+v57b=de5)7'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'omuni.apps.commons.middleware.InterfaceLanguage',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'omuni.urls'

WSGI_APPLICATION = 'omuni.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'south',
    'userena',
    'guardian',
    'easy_thumbnails',
    'omuni.apps.accounts',
    'omuni.apps.budgets',
    'omuni.apps.commons',
    'omuni.apps.govts',
    'omuni.apps.pages',

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
        # loading the django defaults...
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',

        # Add our own context processors
        'django.core.context_processors.request',
        'omuni.apps.commons.context_processors.get_site',
)

FIXTURE_DIRS = (
    os.path.abspath(os.path.join(PROJECT_ROOT, 'fixtures')),
)

# Supported languages for this instance of open muni
gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('he', gettext('Hebrew')),
    ('ar', gettext('Arabic')),
    ('ru', gettext('Russian')),
)

# We use Mozilla's unicode-slugify function so we can slugify
# Hebrew and Arabic correctly, NOT transliterate
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# We use django-userena for user account management.
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
ANONYMOUS_USER_ID = -1  # django-guardian requires it
USERENA_WITHOUT_USERNAMES = True
USERENA_DISABLE_PROFILE_LIST = True
USERENA_DEFAULT_PRIVACY = 'closed'
USERENA_PROFILE_DETAIL_TEMPLATE = 'accounts/profile_detail.html'
USERENA_MUGSHOT_GRAVATAR = True
USERENA_MUGSHOT_DEFAULT = 'monsterid'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
