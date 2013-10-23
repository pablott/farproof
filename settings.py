

# Django settings for farproof project.
import os

FARPROOF_VERSION = '0.1alpha'

FARPROOF_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(FARPROOF_DIR)
STATIC_ROOT = os.path.join(ROOT_DIR, 'static') 


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Pablo Trabajos', 'pablo.trabajos.tamayo@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'jobs.sqlite',					# Or path to database file if using sqlite3.
		'USER': '',								# Not used with sqlite3.
		'PASSWORD': '',							# Not used with sqlite3.
		'HOST': '',								# Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',								# Set to empty string for default. Not used with sqlite3.
	},
	# 'users': {
		# 'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		# 'NAME': 'users.sqlite',          # Or path to database file if using sqlite3.
		# 'USER': '',                      # Not used with sqlite3.
		# 'PASSWORD': '',                  # Not used with sqlite3.
		# 'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
		# 'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
	# }
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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_DIR, 'farproof-html') #.replace('\\', '/'),

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u%8g^o)8b+%xxa-1j^8i@zkv!&0(a8h!pg7j(8lrlc-n1t88dz'

ROOT_URLCONF = 'farproof.urls'

# Folder where PDFs and rendered files (color and separations) are stored.
# Down this path the following structure will be created:
# /client.pk/job.pk/item.pk/pages|render|uploads
CONTENTS_PATH = r'D:\tmp\pdf'

TEMPLATE_DIRS = (
	os.path.join(FARPROOF_DIR, 'templates')#.replace('\\', '/'),
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
	'django.template.loaders.eggs.Loader',
	#Deprecated for Django 1.5:
	#'django.template.loaders.app_directories.load_template_source',
   )

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	# DEPRECATED: https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/#legacy-method
	#'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# https://docs.djangoproject.com/en/1.3/howto/static-files/#with-a-context-processor
TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.request',
	'django.contrib.auth.context_processors.auth',
	'django.contrib.messages.context_processors.messages',
	#'django.contrib.messages.context_processors.request',
	#'djangoapp.app.context_processors.media_url',
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'dajaxice.finders.DajaxiceFinder',
)

STATICFILES_DIRS = (
	#os.path.join(ROOT_DIR, 'static'),
	#'C:\Python27\Lib\site-packages\dajaxice'
	# "/home/special.polls.com/polls/static",
	# "/home/polls.com/polls/static",
	# "/opt/webfiles/common",
)

STATIC_URL = '/static/'

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
		'dajaxice': {
			'handlers': ['console'],
			'level': 'WARNING',
			'propagate': False,
		}
	}
}

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	'django.contrib.admindocs',
	'client_list',
	'django_extensions',
	'django_evolution',
	'dajaxice',
	'dajax',
	'debug_toolbar',
)

DEBUG_TOOLBAR_PANELS = (
	'debug_toolbar.panels.version.VersionDebugPanel',
	'debug_toolbar.panels.timer.TimerDebugPanel',
	'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
	'debug_toolbar.panels.headers.HeaderDebugPanel',
	'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
	'debug_toolbar.panels.template.TemplateDebugPanel',
	'debug_toolbar.panels.sql.SQLDebugPanel',
	'debug_toolbar.panels.signals.SignalDebugPanel',
	'debug_toolbar.panels.logger.LoggingPanel',
)

INTERNAL_IPS = ('127.0.0.1',)

DAJAXICE_DEBUG = True
