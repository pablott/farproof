## Django settings for farproof project.
import os
from os.path import join


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Pablo Trabajos', 'pablo.trabajos.tamayo@gmail.com'),)
MANAGERS = ADMINS

FARPROOF_VERSION = '0.1alpha'
FARPROOF_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(FARPROOF_DIR)
# CONTENTS_PATH:    Folder where PDFs and rendered files are stored.
# PROFILES_PATH:    Folder where ICC profiles are stored.
# TEMP_PATH:        Folder for temporary render files.
CONTENTS_PATH = os.path.abspath('/home/user/farproof/contents')
PROFILES_PATH = os.path.join(CONTENTS_PATH, 'profiles')
TEMP_PATH = os.path.abspath('/home/user/farproof/tmp/render/')

MEDIA_ROOT = CONTENTS_PATH
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(FARPROOF_DIR, 'static-collect')
STATICFILES_DIRS = (os.path.join(FARPROOF_DIR, 'static'),)
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/media/admin/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'jobs.sqlite',  # Or path to database file if using sqlite3.
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    },  # 'users': {
    # 'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    # 'NAME': 'users.sqlite',          # Or path to database file if using sqlite3.
    # 'USER': '',                      # Not used with sqlite3.
    # 'PASSWORD': '',                  # Not used with sqlite3.
    # 'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    # 'PORT': '',                      # Set to empty string for default. Not used with sqlite3.  # }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ES'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u%8g^o)8b+%xxa-1j^8i@zkv!&0(a8h!pg7j(8lrlc-n1t88dz'

ROOT_URLCONF = 'farproof.urls'

TEMPLATE_DIRS = (join(FARPROOF_DIR, 'templates'),)
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # DEPRECATED: https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/#legacy-method
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
# https://docs.djangoproject.com/en/1.3/howto/static-files/#with-a-context-processor
TEMPLATE_CONTEXT_PROCESSORS = (  # 'django.contrib.auth.context_processors.auth',
                                 'django.core.context_processors.debug',
                                 'django.core.context_processors.i18n',
                                 'django.core.context_processors.media',
                                 'django.core.context_processors.static',
                                 'django.core.context_processors.request',
                                 'django.contrib.auth.context_processors.auth',
                                 'django.contrib.messages.context_processors.messages',
                                 # 'django.contrib.messages.context_processors.request',
                                 # 'djangoapp.app.context_processors.media_url',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

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
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
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

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'farproof.client_list',
    'django.contrib.humanize',
    'django_extensions',
    'debug_toolbar',
    'djcelery',
    'celery',
)


## Celery stuff:
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_BACKEND = 'amqp'
CELERY_RESULT_EXCHANGE = 'amqp'
CELERY_IMPORTS = ("farproof.process.process",)
CELERY_TASK_RESULT_EXPIRES = 3600
# CELERY_ALWAYS_EAGER = True
# CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
# CELERY_ACCEPT_CONTENT = ['json',]


## Debug toolbar:
# DEBUG_TOOLBAR_PANELS = [
# 'debug_toolbar.panels.versions.VersionsPanel',
# 'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]
# INTERNAL_IPS = ('127.0.0.1',)

