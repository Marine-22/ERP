import os
from erp.settings.common import *

# Settings specific variables
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))[:-9]

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

# Database connection string
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'erp',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '#H3ll0D0lly#1987',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "../static")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/assets/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''
#

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "../templates"),
    )

# List of installed apps
INSTALLED_APPS = (
    # Some weird django shit
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Load dependencies
    'activelink',
    'ajax_validation',
    'smart_selects',
    'notification',

    # Load libs
    'erp.libs.workflows',

    # Applications
    'erp.apps.internal',
	'erp.apps.fabric',
    'erp.apps.partner',
    'erp.apps.project',
    'erp.apps.reporting',
    'erp.apps.resources',
    'erp.apps.simplewiki',
    'erp.apps.timesheet',
    
    )

# Pipeline settings
PIPELINE = False
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
PIPELINE_VERSION = False

PIPELINE_CSS = {
    'css': {
        'source_filenames': (
            'scripts/jqueryui/jqueryui.css',
            'styles/columnal/columnal.css',
            'styles/style.css',
            'styles/global.css',
            'styles/config.css',
            'scripts/superfish/superfish.css',
            'scripts/formvalidator/validationEngine.jquery.css',
            'scripts/formvalidator/validationEngine.jquery.css',
            'scripts/colorbox/colorbox.css',
            'scripts/fullcalendar/fullcalendar.css',
            'styles/jquery.ganttView.css',
            'styles/chosen.css',
            ),
        'output_filename': 'cache/compressed.r?.css',
        'extra_context': {
            'media': 'screen,projection',
            },
        },
    }

PIPELINE_JS = {
    'js': {
        'source_filenames': (
            'scripts/jquery-1.6.4.min.js',
            'scripts/jqueryui/jquery-ui-1.8.16.custom.min.js',
            'scripts/superfish/superfish.js',
            'scripts/jquery.placeholder.1.2.min.shrink.js',
            'scripts/jquery.dataTables.min.js',
            'scripts/twipsy.js',
            'scripts/formvalidator/jquery.validationEngine.js',
            'scripts/formvalidator/jquery.validationEngine-en.js',
            'scripts/fullcalendar/fullcalendar.min.js',
            'scripts/colorbox/jquery.colorbox-min.js',
            'scripts/date.js',
            'scripts/demo.js',
            'scripts/muse.js',
            'scripts/form.js',
            'scripts/jquery.ganttView.js',
            'scripts/livequery.js',
            'scripts/chosen.jquery.min.js',
            'scripts/validation.js',
            'scripts/erp/loaders.js',
            'scripts/erp/timesheet.js'
            ),
        'output_filename': 'cache/compressed.r?.js',
        }
}

# AD_DNS_NAME = 'mail.iquap.com'
# AD_LDAP_PORT = 389
# AD_SEARCH_DN = 'dc=HQ,dc=IQUAP,dc=LOCAL,ou=MyBusiness,ou=Users,ou=SBSUsers'

# AD_NT4_DOMAIN = 'IQUAP'
# AD_SEARCH_FIELDS = ['mail','givenName','sn','sAMAccountName']
# AD_LDAP_URL = 'ldap://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)

# AUTHENTICATION_BACKENDS = (
#         'core.auth.backend.active_directory.ActiveDirectoryBackend',
#     )
	
LOGIN_EXEMPT_URLS = (
    r'^assets/',
	r'^accounts/login/$'
)

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/accounts/login/'
